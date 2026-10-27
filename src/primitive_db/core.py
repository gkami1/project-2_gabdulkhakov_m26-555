#!/usr/bin/env python3

from primitive_db.constants import (
    COLUMN_TYPE_SEPARATOR,
    ID_COLUMN,
    ID_TYPE,
    VALID_TYPES,
)


def create_table(metadata, table_name, columns):
    """
    Создаёт таблицу. Возвращает обновлённый metadata или None при ошибке.
    """
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None

    parsed_columns = [(ID_COLUMN, ID_TYPE)]
    for column in columns:
        if COLUMN_TYPE_SEPARATOR not in column:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return None
        name, col_type = column.split(COLUMN_TYPE_SEPARATOR, 1)
        if col_type not in VALID_TYPES:
            print(f"Некорректное значение: {col_type}. Попробуйте снова.")
            return None
        parsed_columns.append((name, col_type))

    metadata[table_name] = {"columns": parsed_columns}

    columns_str = ", ".join(f"{name}:{typ}" for name, typ in parsed_columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')
    return metadata


def drop_table(metadata, table_name):
    """Удаляет таблицу. Возвращает обновлённый metadata или None при ошибке."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def list_tables(metadata):
    """Печатает список таблиц."""
    if not metadata:
        print("Список таблиц пуст.")
        return
    for table_name in metadata:
        print(f"- {table_name}")
