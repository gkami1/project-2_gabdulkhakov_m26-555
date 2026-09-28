#!/usr/bin/env python3

import prompt

HELP_TEXT = """<command> exit - выйти из программы
<command> help - справочная информация"""


def welcome():
    print("***")
    print(HELP_TEXT)
    while True:
        command = prompt.string("Введите команду: ").strip().lower()

        if command == "exit":
            break
        elif command == "help":
            print(HELP_TEXT)
        else:
            print("Неизвестная команда")