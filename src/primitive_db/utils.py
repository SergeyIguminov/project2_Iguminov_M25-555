import json


def load_metadata(filepath):
    """
    Загружает данные из JSON-файла.

    Аргументы:
        filepath - Путь к JSON-файлу

    Возвращает - словарь из JSON-файла

    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """
    Сохраняет данные в JSON-файл.

    Args:
        filepath - путь к JSON-файлу
        data - Данные для сохранения в виде словаря
    """
    with open(filepath, "w") as f:
        json.dump(data, f)


def load_table_data(table_path):
    with open(table_path) as f:
        data = json.load(f)
        return data


def save_table_data(table_path, data):
    with open(table_path, "w") as f:
        json.dump(data, f)
