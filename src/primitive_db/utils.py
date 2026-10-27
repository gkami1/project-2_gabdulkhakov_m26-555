#!/usr/bin/env python3

import json
import os

from primitive_db.constants import DATA_DIR, DATA_FILE_EXTENSION


def load_metadata(filepath):
    """Загружает метаданные из JSON-файла. Возвращает {} если файла нет."""
    try:
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_table_path(table_name):
    """Возвращает путь к файлу с данными таблицы."""
    return os.path.join(DATA_DIR, f"{table_name}{DATA_FILE_EXTENSION}")


def load_table_data(table_name):
    """Загружает записи таблицы. Возвращает [] если файла нет."""
    try:
        with open(get_table_path(table_name), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет записи таблицы, при необходимости создаёт директорию data/."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(get_table_path(table_name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def delete_table_data(table_name):
    """Удаляет файл с данными таблицы, если он существует."""
    path = get_table_path(table_name)
    if os.path.exists(path):
        os.remove(path)
