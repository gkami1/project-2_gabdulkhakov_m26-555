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


def get_column_types(metadata, table_name):
    """Возвращает словарь {столбец: тип} для таблицы."""
    return dict(metadata[table_name]["columns"])


def is_valid_type(value, column_type):
    """Проверяет, что значение соответствует типу столбца."""
    if column_type == "bool":
        return isinstance(value, bool)
    if column_type == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    return isinstance(value, str)


def check_table_exists(metadata, table_name):
    """Печатает ошибку и возвращает False, если таблицы нет."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return False
    return True


def check_clause(metadata, table_name, clause):
    """Проверяет столбцы и типы значений в условии where/set."""
    column_types = get_column_types(metadata, table_name)
    for column, value in clause.items():
        if column not in column_types:
            print(f'Ошибка: Столбец "{column}" не существует в таблице "{table_name}".')
            return False
        if not is_valid_type(value, column_types[column]):
            print(f"Некорректное значение: {value}. Попробуйте снова.")
            return False
    return True


def matches(record, where_clause):
    """Проверяет, подходит ли запись под условие where."""
    return all(record.get(column) == value for column, value in where_clause.items())


def insert(metadata, table_name, table_data, values):
    """Добавляет запись в таблицу. Возвращает обновлённые данные или None."""
    if not check_table_exists(metadata, table_name):
        return None

    columns = metadata[table_name]["columns"][1:]
    if len(values) != len(columns):
        print(
            f"Некорректное значение: ожидалось значений: {len(columns)}, "
            f"получено: {len(values)}. Попробуйте снова."
        )
        return None

    for value, (_, column_type) in zip(values, columns):
        if not is_valid_type(value, column_type):
            print(f"Некорректное значение: {value}. Попробуйте снова.")
            return None

    new_id = max((record[ID_COLUMN] for record in table_data), default=0) + 1
    record = {ID_COLUMN: new_id}
    record.update((name, value) for value, (name, _) in zip(values, columns))
    table_data.append(record)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return table_data


def select(metadata, table_name, table_data, where_clause=None):
    """Возвращает записи таблицы, подходящие под условие, или None при ошибке."""
    if not check_table_exists(metadata, table_name):
        return None
    if where_clause is None:
        return table_data
    if not check_clause(metadata, table_name, where_clause):
        return None
    return [record for record in table_data if matches(record, where_clause)]


def update(metadata, table_name, table_data, set_clause, where_clause):
    """Обновляет записи по условию. Возвращает обновлённые данные или None."""
    if not check_table_exists(metadata, table_name):
        return None
    if ID_COLUMN in set_clause:
        print(f"Некорректное значение: {ID_COLUMN}. Попробуйте снова.")
        return None
    if not check_clause(metadata, table_name, {**set_clause, **where_clause}):
        return None

    found = [record for record in table_data if matches(record, where_clause)]
    if not found:
        print("Записи, удовлетворяющие условию, не найдены.")
        return None
    for record in found:
        record.update(set_clause)
        print(
            f'Запись с ID={record[ID_COLUMN]} в таблице "{table_name}" '
            "успешно обновлена."
        )
    return table_data


def delete(metadata, table_name, table_data, where_clause):
    """Удаляет записи по условию. Возвращает обновлённые данные или None."""
    if not check_table_exists(metadata, table_name):
        return None
    if not check_clause(metadata, table_name, where_clause):
        return None

    found = [record for record in table_data if matches(record, where_clause)]
    if not found:
        print("Записи, удовлетворяющие условию, не найдены.")
        return None
    for record in found:
        table_data.remove(record)
        print(
            f"Запись с ID={record[ID_COLUMN]} успешно удалена "
            f'из таблицы "{table_name}".'
        )
    return table_data


def info(metadata, table_name, table_data):
    """Печатает схему таблицы и количество записей."""
    if not check_table_exists(metadata, table_name):
        return
    columns = metadata[table_name]["columns"]
    columns_str = ", ".join(f"{name}:{typ}" for name, typ in columns)
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {columns_str}")
    print(f"Количество записей: {len(table_data)}")
