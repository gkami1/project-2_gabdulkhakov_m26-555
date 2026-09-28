#!/usr/bin/env python3

import shlex

import prompt

from src.primitive_db.core import create_table, drop_table, list_tables
from src.primitive_db.utils import load_metadata, save_metadata

DB_FILE = "db_meta.json"


def print_help():
    """Prints the help message for the current mode."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    print("***База данных***")
    print_help()

    while True:
        user_input = prompt.string(">>>Введите команду: ").strip()

        try:
            args = shlex.split(user_input)
        except ValueError as exc:
            print(f"Ошибка разбора команды: {exc}. Попробуйте снова.")
            continue

        command = args[0]
        metadata = load_metadata(DB_FILE)

        if command == "exit":
            break

        elif command == "help":
            print_help()

        elif command == "list_tables":
            list_tables(metadata)

        elif command == "create_table":
            if len(args) < 3:
                print("Некорректное значение: не указаны столбцы. Попробуйте снова.")
                continue
            table_name = args[1]
            columns = args[2:]
            updated = create_table(metadata, table_name, columns)
            if updated is not None:
                save_metadata(DB_FILE, updated)

        elif command == "drop_table":
            if len(args) != 2:
                print("Некорректное значение: нужно имя таблицы. Попробуйте снова.")
                continue
            updated = drop_table(metadata, args[1])
            if updated is not None:
                save_metadata(DB_FILE, updated)

        else:
            print(f"Функции {command} нет. Попробуйте снова.")
