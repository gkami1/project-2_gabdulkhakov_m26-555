"""Константы проекта."""

# Файл с метаданными таблиц
META_FILE = "db_meta.json"

# Хранение данных таблиц: data/<таблица>.json
DATA_DIR = "data"
DATA_FILE_EXTENSION = ".json"

# Схема таблиц
VALID_TYPES = ("int", "str", "bool")
ID_COLUMN = "ID"
ID_TYPE = "int"
COLUMN_TYPE_SEPARATOR = ":"

# Разбор команд
PUNCTUATION_CHARS = "=,()"
QUOTE_CHARS = "\"'"
EQUALS_SIGN = "="
COMMA = ","
OPEN_BRACKET = "("
CLOSE_BRACKET = ")"
TRUE_LITERAL = "true"
FALSE_LITERAL = "false"

# Ключевые слова команд
KEYWORD_INTO = "into"
KEYWORD_FROM = "from"
KEYWORD_VALUES = "values"
KEYWORD_WHERE = "where"
KEYWORD_SET = "set"

# Сообщения обработчика ошибок
MSG_FILE_NOT_FOUND = (
    "Ошибка: Файл данных не найден. Возможно, база данных не инициализирована."
)
MSG_UNEXPECTED_ERROR = "Произошла непредвиденная ошибка: {}"
