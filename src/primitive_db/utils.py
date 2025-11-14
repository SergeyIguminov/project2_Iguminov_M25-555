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
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении файла {filepath}: {e}")
