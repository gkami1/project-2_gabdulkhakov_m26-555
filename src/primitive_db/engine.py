#!/usr/bin/env python3

import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.constants import META_FILE
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
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values "
        "(<значение1>, <значение2>, ...) - создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where <столбец> = <значение> "
        "- прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where <столбец> = <значение> "
        "- удалить запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def print_records(metadata, table_name, records):
    """Выводит записи в виде таблицы prettytable."""
    if not records:
        print("Записи не найдены.")
        return
    table = PrettyTable()
    table.field_names = [name for name, _ in metadata[table_name]["columns"]]
    for record in records:
        table.add_row([record.get(name) for name in table.field_names])
    table.align = "c"
    print(table)


def handle_insert(metadata, user_input):
    """Обрабатывает команду insert."""
    table_name, values = parse_insert(user_input)
    data = insert(metadata, table_name, load_table_data(table_name), values)
    if data is not None:
        save_table_data(table_name, data)


def handle_select(metadata, user_input):
    """Обрабатывает команду select."""
    table_name, where_clause = parse_select(user_input)
    records = select(metadata, table_name, load_table_data(table_name), where_clause)
    if records is not None:
        print_records(metadata, table_name, records)


def handle_update(metadata, user_input):
    """Обрабатывает команду update."""
    table_name, set_clause, where_clause = parse_update(user_input)
    data = update(
        metadata, table_name, load_table_data(table_name), set_clause, where_clause
    )
    if data is not None:
        save_table_data(table_name, data)


def handle_delete(metadata, user_input):
    """Обрабатывает команду delete."""
    table_name, where_clause = parse_delete(user_input)
    data = delete(metadata, table_name, load_table_data(table_name), where_clause)
    if data is not None:
        save_table_data(table_name, data)


def run():
    """Главный цикл программы."""
    print("***База данных***")
    print_help()

    while True:
        try:
            user_input = prompt.string(">>>Введите команду: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        try:
            args = shlex.split(user_input)
        except ValueError as exc:
            print(f"Ошибка разбора команды: {exc}. Попробуйте снова.")
            continue

        if not args:
            continue

        command = args[0]
        metadata = load_metadata(META_FILE)

        try:
            if command == "exit":
                break

            elif command == "help":
                print_help()

            elif command == "list_tables":
                list_tables(metadata)

            elif command == "create_table":
                if len(args) < 3:
                    print(
                        "Некорректное значение: не указаны столбцы. Попробуйте снова."
                    )
                    continue
                updated = create_table(metadata, args[1], args[2:])
                if updated is not None:
                    save_metadata(META_FILE, updated)

            elif command == "drop_table":
                if len(args) != 2:
                    print("Некорректное значение: нужно имя таблицы. Попробуйте снова.")
                    continue
                updated = drop_table(metadata, args[1])
                if updated is not None:
                    save_metadata(META_FILE, updated)
                    delete_table_data(args[1])

            elif command == "insert":
                handle_insert(metadata, user_input)

            elif command == "select":
                handle_select(metadata, user_input)

            elif command == "update":
                handle_update(metadata, user_input)

            elif command == "delete":
                handle_delete(metadata, user_input)

            elif command == "info":
                if len(args) != 2:
                    print("Некорректное значение: нужно имя таблицы. Попробуйте снова.")
                    continue
                info(metadata, args[1], load_table_data(args[1]))

            else:
                print(f"Функции {command} нет. Попробуйте снова.")

        except ValueError as exc:
            # Ошибки разбора values/where/set
            print(f"Некорректное значение: {exc}. Попробуйте снова.")
