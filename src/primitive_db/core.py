#!/usr/bin/env python3

from primitive_db.constants import (
    ACTION_DELETE_RECORDS,
    ACTION_DROP_TABLE,
    COLUMN_LIST_SEPARATOR,
    COLUMN_TYPE_SEPARATOR,
    COLUMNS_KEY,
    ID_COLUMN,
    ID_TYPE,
    MSG_COLUMN_NOT_EXISTS,
    MSG_INFO_COLUMNS,
    MSG_INFO_RECORDS_COUNT,
    MSG_INFO_TABLE,
    MSG_INVALID_VALUE,
    MSG_NO_MATCHING_RECORDS,
    MSG_NO_TABLES,
    MSG_RECORD_DELETED,
    MSG_RECORD_INSERTED,
    MSG_RECORD_UPDATED,
    MSG_TABLE_CREATED,
    MSG_TABLE_DROPPED,
    MSG_TABLE_EXISTS,
    MSG_TABLE_LIST_ITEM,
    MSG_TABLE_NOT_EXISTS,
    MSG_WRONG_VALUES_COUNT,
    TYPE_BOOL,
    TYPE_INT,
    VALID_TYPES,
)
from primitive_db.decorators import confirm_action, handle_db_errors, log_time


def format_columns(columns):
    """Форматирует столбцы в строку вида ID:int, name:str."""
    return COLUMN_LIST_SEPARATOR.join(
        f"{name}{COLUMN_TYPE_SEPARATOR}{column_type}" for name, column_type in columns
    )


def parse_column(column):
    """Разбирает описание столбца name:type и проверяет тип."""
    name, separator, column_type = column.partition(COLUMN_TYPE_SEPARATOR)
    if not name or not separator:
        raise ValueError(MSG_INVALID_VALUE.format(column))
    if column_type not in VALID_TYPES:
        raise ValueError(MSG_INVALID_VALUE.format(column_type))
    return name, column_type


def check_table_exists(metadata, table_name):
    """Выбрасывает KeyError, если таблицы нет."""
    if table_name not in metadata:
        raise KeyError(MSG_TABLE_NOT_EXISTS.format(table_name))


def is_valid_type(value, column_type):
    """Проверяет, что значение соответствует типу столбца."""
    if column_type == TYPE_BOOL:
        return isinstance(value, bool)
    if column_type == TYPE_INT:
        return isinstance(value, int) and not isinstance(value, bool)
    return isinstance(value, str)


def check_value(value, column_type):
    """Выбрасывает ValueError, если значение не подходит по типу."""
    if not is_valid_type(value, column_type):
        raise ValueError(MSG_INVALID_VALUE.format(value))


def check_clause(metadata, table_name, clause):
    """Проверяет столбцы и типы значений в условии where/set."""
    column_types = dict(metadata[table_name][COLUMNS_KEY])
    for column, value in clause.items():
        if column not in column_types:
            raise KeyError(MSG_COLUMN_NOT_EXISTS.format(column, table_name))
        check_value(value, column_types[column])


def matches(record, where_clause):
    """Проверяет, подходит ли запись под условие where."""
    return all(record.get(column) == value for column, value in where_clause.items())


def find_records(table_data, where_clause):
    """Возвращает записи, подходящие под условие where."""
    return [record for record in table_data if matches(record, where_clause)]


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создаёт таблицу со столбцом ID. Возвращает обновлённые метаданные."""
    if table_name in metadata:
        raise ValueError(MSG_TABLE_EXISTS.format(table_name))

    parsed_columns = [(ID_COLUMN, ID_TYPE)]
    parsed_columns.extend(parse_column(column) for column in columns)
    metadata[table_name] = {COLUMNS_KEY: parsed_columns}
    print(MSG_TABLE_CREATED.format(table_name, format_columns(parsed_columns)))
    return metadata


@handle_db_errors
@confirm_action(ACTION_DROP_TABLE)
def drop_table(metadata, table_name):
    """Удаляет таблицу. Возвращает обновлённые метаданные."""
    check_table_exists(metadata, table_name)
    del metadata[table_name]
    print(MSG_TABLE_DROPPED.format(table_name))
    return metadata


def list_tables(metadata):
    """Печатает список таблиц."""
    if not metadata:
        print(MSG_NO_TABLES)
    for table_name in metadata:
        print(MSG_TABLE_LIST_ITEM.format(table_name))


@handle_db_errors
@log_time
def insert(metadata, table_name, table_data, values):
    """Добавляет запись с новым ID. Возвращает обновлённые данные."""
    check_table_exists(metadata, table_name)
    columns = metadata[table_name][COLUMNS_KEY][1:]
    if len(values) != len(columns):
        count_error = MSG_WRONG_VALUES_COUNT.format(len(columns), len(values))
        raise ValueError(MSG_INVALID_VALUE.format(count_error))
    for value, (_, column_type) in zip(values, columns):
        check_value(value, column_type)

    new_id = max((record[ID_COLUMN] for record in table_data), default=0) + 1
    record = {ID_COLUMN: new_id}
    record.update((name, value) for value, (name, _) in zip(values, columns))
    table_data.append(record)
    print(MSG_RECORD_INSERTED.format(new_id, table_name))
    return table_data


@handle_db_errors
@log_time
def select(metadata, table_name, table_data, where_clause=None):
    """Возвращает записи таблицы, подходящие под условие where."""
    check_table_exists(metadata, table_name)
    if where_clause is None:
        return table_data
    check_clause(metadata, table_name, where_clause)
    return find_records(table_data, where_clause)


@handle_db_errors
def update(metadata, table_name, table_data, set_clause, where_clause):
    """Обновляет записи по условию. Возвращает обновлённые данные."""
    check_table_exists(metadata, table_name)
    if ID_COLUMN in set_clause:
        raise ValueError(MSG_INVALID_VALUE.format(ID_COLUMN))
    check_clause(metadata, table_name, set_clause)
    check_clause(metadata, table_name, where_clause)

    found = find_records(table_data, where_clause)
    if not found:
        print(MSG_NO_MATCHING_RECORDS)
        return None
    for record in found:
        record.update(set_clause)
        print(MSG_RECORD_UPDATED.format(record[ID_COLUMN], table_name))
    return table_data


@handle_db_errors
@confirm_action(ACTION_DELETE_RECORDS)
def delete(metadata, table_name, table_data, where_clause):
    """Удаляет записи по условию. Возвращает обновлённые данные."""
    check_table_exists(metadata, table_name)
    check_clause(metadata, table_name, where_clause)

    found = find_records(table_data, where_clause)
    if not found:
        print(MSG_NO_MATCHING_RECORDS)
        return None
    for record in found:
        table_data.remove(record)
        print(MSG_RECORD_DELETED.format(record[ID_COLUMN], table_name))
    return table_data


@handle_db_errors
def info(metadata, table_name, table_data):
    """Печатает схему таблицы и количество записей."""
    check_table_exists(metadata, table_name)
    print(MSG_INFO_TABLE.format(table_name))
    print(MSG_INFO_COLUMNS.format(format_columns(metadata[table_name][COLUMNS_KEY])))
    print(MSG_INFO_RECORDS_COUNT.format(len(table_data)))
