#!/usr/bin/env python3

import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.constants import (
    CMD_CREATE_TABLE,
    CMD_DELETE,
    CMD_DROP_TABLE,
    CMD_EXIT,
    CMD_HELP,
    CMD_INFO,
    CMD_INSERT,
    CMD_LIST_TABLES,
    CMD_SELECT,
    CMD_UPDATE,
    COLUMNS_KEY,
    CREATE_TABLE_MIN_ARGS,
    HELP_TEXT,
    INPUT_PROMPT,
    META_FILE,
    MSG_COMMAND_PARSE_ERROR,
    MSG_INVALID_VALUE,
    MSG_NO_COLUMNS,
    MSG_NO_RECORDS,
    MSG_TABLE_NAME_REQUIRED,
    MSG_UNKNOWN_COMMAND,
    TABLE_ALIGN,
    TABLE_COMMAND_ARGS,
    WELCOME_TITLE,
)
from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    list_tables,
    select,
    update,
)
from primitive_db.decorators import handle_db_errors
from primitive_db.parser import (
    parse_delete,
    parse_insert,
    parse_select,
    parse_update,
)
from primitive_db.utils import (
    delete_table_data,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help():
    """Печатает справку по командам."""
    print(HELP_TEXT)


def print_records(metadata, table_name, records):
    """Выводит записи в виде таблицы prettytable."""
    if not records:
        print(MSG_NO_RECORDS)
        return
    table = PrettyTable()
    table.field_names = [name for name, _ in metadata[table_name][COLUMNS_KEY]]
    for record in records:
        table.add_row([record.get(name) for name in table.field_names])
    table.align = TABLE_ALIGN
    print(table)


def get_table_name(args):
    """Возвращает имя таблицы из аргументов вида <команда> <таблица>."""
    if len(args) != TABLE_COMMAND_ARGS:
        raise ValueError(MSG_INVALID_VALUE.format(MSG_TABLE_NAME_REQUIRED))
    return args[1]


@handle_db_errors
def handle_create_table(metadata, args):
    """Обрабатывает команду create_table."""
    if len(args) < CREATE_TABLE_MIN_ARGS:
        raise ValueError(MSG_INVALID_VALUE.format(MSG_NO_COLUMNS))
    updated = create_table(metadata, args[1], args[2:])
    if updated is not None:
        save_metadata(META_FILE, updated)


@handle_db_errors
def handle_drop_table(metadata, args):
    """Обрабатывает команду drop_table и удаляет файл данных таблицы."""
    table_name = get_table_name(args)
    updated = drop_table(metadata, table_name)
    if updated is not None:
        save_metadata(META_FILE, updated)
        delete_table_data(table_name)


@handle_db_errors
def handle_info(metadata, args):
    """Обрабатывает команду info."""
    table_name = get_table_name(args)
    info(metadata, table_name, load_table_data(table_name))


@handle_db_errors
def handle_insert(metadata, user_input):
    """Обрабатывает команду insert."""
    table_name, values = parse_insert(user_input)
    data = insert(metadata, table_name, load_table_data(table_name), values)
    if data is not None:
        save_table_data(table_name, data)


@handle_db_errors
def handle_select(metadata, user_input):
    """Обрабатывает команду select."""
    table_name, where_clause = parse_select(user_input)
    records = select(metadata, table_name, load_table_data(table_name), where_clause)
    if records is not None:
        print_records(metadata, table_name, records)


@handle_db_errors
def handle_update(metadata, user_input):
    """Обрабатывает команду update."""
    table_name, set_clause, where_clause = parse_update(user_input)
    data = update(
        metadata, table_name, load_table_data(table_name), set_clause, where_clause
    )
    if data is not None:
        save_table_data(table_name, data)


@handle_db_errors
def handle_delete(metadata, user_input):
    """Обрабатывает команду delete."""
    table_name, where_clause = parse_delete(user_input)
    data = delete(metadata, table_name, load_table_data(table_name), where_clause)
    if data is not None:
        save_table_data(table_name, data)


# Команды, которым нужны разобранные shlex аргументы
ARGS_HANDLERS = {
    CMD_CREATE_TABLE: handle_create_table,
    CMD_DROP_TABLE: handle_drop_table,
    CMD_INFO: handle_info,
}

# Команды, которые разбираются парсером из исходной строки
INPUT_HANDLERS = {
    CMD_INSERT: handle_insert,
    CMD_SELECT: handle_select,
    CMD_UPDATE: handle_update,
    CMD_DELETE: handle_delete,
}


def run():
    """Главный цикл программы."""
    print(WELCOME_TITLE)
    print_help()

    while True:
        try:
            user_input = prompt.string(INPUT_PROMPT).strip()
        except (EOFError, KeyboardInterrupt):
            break

        try:
            args = shlex.split(user_input)
        except ValueError as exc:
            print(MSG_COMMAND_PARSE_ERROR.format(exc))
            continue

        if not args:
            continue

        command = args[0]
        metadata = load_metadata(META_FILE)

        if command == CMD_EXIT:
            break
        elif command == CMD_HELP:
            print_help()
        elif command == CMD_LIST_TABLES:
            list_tables(metadata)
        elif command in ARGS_HANDLERS:
            ARGS_HANDLERS[command](metadata, args)
        elif command in INPUT_HANDLERS:
            INPUT_HANDLERS[command](metadata, user_input)
        else:
            print(MSG_UNKNOWN_COMMAND.format(command))
