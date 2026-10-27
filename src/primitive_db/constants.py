"""Константы проекта."""

# Файл с метаданными таблиц
META_FILE = "db_meta.json"

# Хранение данных таблиц: data/<таблица>.json
DATA_DIR = "data"
DATA_FILE_EXTENSION = ".json"

# Схема таблиц
TYPE_INT = "int"
TYPE_STR = "str"
TYPE_BOOL = "bool"
VALID_TYPES = (TYPE_INT, TYPE_STR, TYPE_BOOL)
ID_COLUMN = "ID"
ID_TYPE = TYPE_INT
COLUMNS_KEY = "columns"
COLUMN_TYPE_SEPARATOR = ":"
COLUMN_LIST_SEPARATOR = ", "

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

# Сообщения операций с таблицами и данными
MSG_INVALID_VALUE = "Некорректное значение: {}. Попробуйте снова."
MSG_WRONG_VALUES_COUNT = "ожидалось значений: {}, получено: {}"
MSG_TABLE_EXISTS = 'Ошибка: Таблица "{}" уже существует.'
MSG_TABLE_NOT_EXISTS = 'Ошибка: Таблица "{}" не существует.'
MSG_COLUMN_NOT_EXISTS = 'Ошибка: Столбец "{}" не существует в таблице "{}".'
MSG_TABLE_CREATED = 'Таблица "{}" успешно создана со столбцами: {}'
MSG_TABLE_DROPPED = 'Таблица "{}" успешно удалена.'
MSG_NO_TABLES = "Список таблиц пуст."
MSG_TABLE_LIST_ITEM = "- {}"
MSG_RECORD_INSERTED = 'Запись с ID={} успешно добавлена в таблицу "{}".'
MSG_RECORD_UPDATED = 'Запись с ID={} в таблице "{}" успешно обновлена.'
MSG_RECORD_DELETED = 'Запись с ID={} успешно удалена из таблицы "{}".'
MSG_NO_MATCHING_RECORDS = "Записи, удовлетворяющие условию, не найдены."
MSG_INFO_TABLE = "Таблица: {}"
MSG_INFO_COLUMNS = "Столбцы: {}"
MSG_INFO_RECORDS_COUNT = "Количество записей: {}"

# Пояснения к ошибкам разбора
MSG_UNCLOSED_QUOTE = "незакрытая кавычка"
MSG_EXPECTED_KEYWORD = "ожидалось ключевое слово {}"
MSG_NO_TABLE_NAME = "не указано имя таблицы"
MSG_EMPTY_CLAUSE = "пустое условие"
MSG_NO_VALUES = "нет значений"
MSG_EMPTY_VALUE = "пустое значение"
TOKEN_SEPARATOR = " "

# Подтверждение опасных операций
CONFIRM_PROMPT = 'Вы уверены, что хотите выполнить "{}"? [y/n]: '
CONFIRM_YES = "y"
MSG_ACTION_CANCELLED = "Операция отменена."
ACTION_DROP_TABLE = "удаление таблицы"
ACTION_DELETE_RECORDS = "удаление записи"
