#!/usr/bin/env python3

from primitive_db.constants import MSG_FILE_NOT_FOUND, MSG_UNEXPECTED_ERROR


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
