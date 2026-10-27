#!/usr/bin/env python3

import time

import prompt

from primitive_db.constants import (
    CONFIRM_PROMPT,
    CONFIRM_YES,
    MSG_ACTION_CANCELLED,
    MSG_EXECUTION_TIME,
    MSG_FILE_NOT_FOUND,
    MSG_UNEXPECTED_ERROR,
)


def copy_metadata(wrapper, func):
    """Переносит имя и docstring исходной функции на обёртку."""
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


def handle_db_errors(func):
    """Перехватывает ошибки операций с БД и печатает сообщение.

    Текст сообщения для KeyError и ValueError передаётся в самом исключении.
    При ошибке обёрнутая функция возвращает None.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(MSG_FILE_NOT_FOUND)
        except KeyError as exc:
            # str(KeyError) добавляет кавычки, поэтому берём аргумент напрямую
            print(exc.args[0])
        except ValueError as exc:
            print(exc)
        except Exception as exc:
            print(MSG_UNEXPECTED_ERROR.format(exc))
        return None

    return copy_metadata(wrapper, func)


def confirm_action(action_name):
    """Фабрика декораторов: запрашивает подтверждение перед действием.

    Если пользователь ввёл не "y", операция отменяется и возвращается None.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            answer = prompt.string(CONFIRM_PROMPT.format(action_name))
            if answer.strip().lower() != CONFIRM_YES:
                print(MSG_ACTION_CANCELLED)
                return None
            return func(*args, **kwargs)

        return copy_metadata(wrapper, func)

    return decorator


def log_time(func):
    """Печатает время выполнения функции."""

    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        print(MSG_EXECUTION_TIME.format(func.__name__, time.monotonic() - start))
        return result

    return copy_metadata(wrapper, func)
