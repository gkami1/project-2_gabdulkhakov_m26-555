#!/usr/bin/env python3

import shlex

from primitive_db.constants import (
    CLOSE_BRACKET,
    COMMA,
    EQUALS_SIGN,
    FALSE_LITERAL,
    KEYWORD_FROM,
    KEYWORD_INTO,
    KEYWORD_SET,
    KEYWORD_VALUES,
    KEYWORD_WHERE,
    MSG_EMPTY_CLAUSE,
    MSG_EMPTY_VALUE,
    MSG_EXPECTED_KEYWORD,
    MSG_INVALID_VALUE,
    MSG_NO_TABLE_NAME,
    MSG_NO_VALUES,
    MSG_UNCLOSED_QUOTE,
    OPEN_BRACKET,
    PUNCTUATION_CHARS,
    QUOTE_CHARS,
    TOKEN_SEPARATOR,
    TRUE_LITERAL,
)


def tokenize(text):
    """Разбивает команду на токены, кавычки у строк сохраняются."""
    lexer = shlex.shlex(text, posix=False, punctuation_chars=PUNCTUATION_CHARS)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:
        raise ValueError(MSG_INVALID_VALUE.format(MSG_UNCLOSED_QUOTE))


def invalid_tokens(tokens, empty_message):
    """Сообщение об ошибке для некорректного фрагмента команды."""
    return MSG_INVALID_VALUE.format(TOKEN_SEPARATOR.join(tokens) or empty_message)


def expected_keyword(keyword):
    """Сообщение об отсутствующем ключевом слове."""
    return MSG_INVALID_VALUE.format(MSG_EXPECTED_KEYWORD.format(keyword))


def parse_value(token):
    """Преобразует токен в значение: строку в кавычках, bool или int."""
    if len(token) >= 2 and token[0] in QUOTE_CHARS and token[-1] == token[0]:
        return token[1:-1]
    if token.lower() == TRUE_LITERAL:
        return True
    if token.lower() == FALSE_LITERAL:
        return False
    try:
        return int(token)
    except ValueError:
        # Строка без кавычек
        return token


def split_by_comma(tokens):
    """Делит список токенов на группы по запятым."""
    groups = [[]]
    for token in tokens:
        if token == COMMA:
            groups.append([])
        else:
            groups[-1].append(token)
    return groups


def parse_assignment(tokens):
    """Разбирает токены вида <столбец> = <значение> в пару (столбец, значение)."""
    if len(tokens) != 3 or tokens[1] != EQUALS_SIGN:
        raise ValueError(invalid_tokens(tokens, MSG_EMPTY_CLAUSE))
    return tokens[0], parse_value(tokens[2])


def parse_where(tokens):
    """Разбирает условие where: ['age', '=', '28'] -> {'age': 28}."""
    column, value = parse_assignment(tokens)
    return {column: value}


def parse_set(tokens):
    """Разбирает set: ['age', '=', '29', ',', ...] -> {'age': 29, ...}."""
    return dict(parse_assignment(group) for group in split_by_comma(tokens))


def parse_values(tokens):
    """Разбирает список значений в скобках: (<значение1>, <значение2>, ...)."""
    if len(tokens) < 3 or tokens[0] != OPEN_BRACKET or tokens[-1] != CLOSE_BRACKET:
        raise ValueError(invalid_tokens(tokens, MSG_NO_VALUES))
    values = []
    for group in split_by_comma(tokens[1:-1]):
        if len(group) != 1:
            raise ValueError(invalid_tokens(group, MSG_EMPTY_VALUE))
        values.append(parse_value(group[0]))
    return values


def expect_keyword(tokens, index, keyword):
    """Проверяет, что на позиции index стоит ключевое слово keyword."""
    if len(tokens) <= index or tokens[index].lower() != keyword:
        raise ValueError(expected_keyword(keyword))


def find_keyword(tokens, keyword):
    """Возвращает позицию ключевого слова или None."""
    for index, token in enumerate(tokens):
        if token.lower() == keyword:
            return index
    return None


def parse_insert(text):
    """insert into <таблица> values (...) -> (таблица, значения)."""
    tokens = tokenize(text)
    expect_keyword(tokens, 1, KEYWORD_INTO)
    expect_keyword(tokens, 3, KEYWORD_VALUES)
    return tokens[2], parse_values(tokens[4:])


def parse_select(text):
    """select from <таблица> [where ...] -> (таблица, условие или None)."""
    tokens = tokenize(text)
    expect_keyword(tokens, 1, KEYWORD_FROM)
    if len(tokens) < 3:
        raise ValueError(MSG_INVALID_VALUE.format(MSG_NO_TABLE_NAME))
    if len(tokens) == 3:
        return tokens[2], None
    expect_keyword(tokens, 3, KEYWORD_WHERE)
    return tokens[2], parse_where(tokens[4:])


def parse_update(text):
    """update <таблица> set ... where ... -> (таблица, set, where)."""
    tokens = tokenize(text)
    expect_keyword(tokens, 2, KEYWORD_SET)
    where_index = find_keyword(tokens, KEYWORD_WHERE)
    if where_index is None:
        raise ValueError(expected_keyword(KEYWORD_WHERE))
    set_clause = parse_set(tokens[3:where_index])
    where_clause = parse_where(tokens[where_index + 1 :])
    return tokens[1], set_clause, where_clause


def parse_delete(text):
    """delete from <таблица> where ... -> (таблица, условие)."""
    tokens = tokenize(text)
    expect_keyword(tokens, 1, KEYWORD_FROM)
    expect_keyword(tokens, 3, KEYWORD_WHERE)
    return tokens[2], parse_where(tokens[4:])
