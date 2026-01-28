import os

from prettytable import PrettyTable

import src.primitive_db.utils as utils

TABLE_DATA_DIR = "data"


def create_table(metadata, table_name, columns):
    """
    Создаёт таблицу
    Перед этим проверяет что нет похожей, что нет одинаковых столбцов и
    проверяет корректность типов данных
    После этого сохраняет всё в отдельный файл
    """
    if table_name not in list(metadata.keys()):
        table_data = {}
        table_data["ID:int"] = []
        if columns:
            count_columns = 0  # Для безымянных колонн
            for column in columns:
                count_columns += 1
                if ":" in column:
                    col_name = column.split(sep=":")[0]
                    col_type = column.split(sep=":")[1]
                    if not col_name:
                        col_name = "col" + str(count_columns)
                    if "=" in col_name:
                        print(
                            f"Недопустимый символ '=' в имени "
                            f"столбца: {col_name}. Попробуйте снова."
                        )
                        return metadata
                    if col_type not in ["int", "str", "bool"]:
                        print(f"Некорректное значение: {col_type}. Попробуйте снова.")
                        return metadata
                    else:
                        table_data[col_name + ":" + col_type] = []
                else:
                    print(f"Некорректная инициализация столбца: {column}.")
                    return metadata
        print(
            f"Таблица '{table_name}' успешно создана со "
            f"столбцами: {[col_name for col_name in list(table_data.keys())]}"
        )
        metadata[table_name] = table_data
        os.makedirs(TABLE_DATA_DIR, exist_ok=True)
        with open(TABLE_DATA_DIR + "/" + table_name + ".json", "w") as file:
            file.write(str(dict()))
        return metadata
    else:
        print(f"Ошибка: Таблица '{table_name}' уже существует.")
        return metadata


def insert(metadata, table_name, values):
    """
    Заполняет таблицу данными
    Проверяет что такая таблица существет,
    проверяет корректность типа данных и их соответствие
    """
    table_path = TABLE_DATA_DIR + "/" + table_name + ".json"
    if table_name not in list(metadata.keys()):
        print(f"Ошибка: Таблица '{table_name}' не существует.")
        return {}
    else:
        table_data = utils.load_table_data(table_path)
        if len(list(metadata[table_name].keys())) - 1 == len(values):
            table_entry = {}
            id_entry = str(len(table_data) + 1)
            columns = list(metadata[table_name].keys())
            columns.pop(0)  # Игнорируем ID:int
            for i in range(len(columns)):
                col_name = columns[i].split(sep=":")[0]
                col_type = columns[i].split(sep=":")[1]
                match col_type:
                    case "int":
                        if not isinstance(values[i], int):
                            print(
                                f"Ошибка: тип переменной {values[i]} не "
                                f"соответствует типу "
                                f"столбца {col_name + ":" + col_type}."
                            )
                            return table_data
                    case "str":
                        if not isinstance(values[i], str):
                            print(
                                f"Ошибка: тип переменной {values[i]} не "
                                f"соответствует типу "
                                f"столбца {col_name + ":" + col_type}."
                            )
                            return table_data
                    case "bool":
                        if not isinstance(values[i], bool):
                            print(
                                f"Ошибка: тип переменной {values[i]} не "
                                f"соответствует типу "
                                f"столбца {col_name + ":" + col_type}."
                            )
                            return table_data
                table_entry[col_name] = values[i]
            table_data[id_entry] = table_entry
            utils.save_table_data(table_path, table_data)
            print(f"Запись с ID={id_entry} успешно добавлена в таблицу {table_name}.")
            return table_data
        else:
            print("Ошибка: Число переменных не соответствует числу столбцов.")
            return table_data


def select(table_data, where_clause=None):
    """
    Метод реализует показ данных отдельных столбцов из таблицы c фильтрацией where
    """
    if where_clause:
        select_data = {}
        col_name = list(where_clause.keys())[0]
        col_value = where_clause[col_name]
        if col_name == "ID":
            for key in list(table_data.keys()):
                if int(key) == col_value:
                    select_data[key] = table_data[key]
            return select_data
        else:
            for key in list(table_data.keys()):
                if table_data[key][col_name] == col_value:
                    select_data[key] = table_data[key]
            return select_data
    else:
        return table_data


def update(table_data, set_clause, where_clause):
    """
    Фильтрует записи по where_clause и обновляет в них поля по set_clause
    """
    set_name = list(set_clause.keys())[0]
    set_value = set_clause[set_name]
    where_name = list(where_clause.keys())[0]
    where_value = where_clause[where_name]
    if set_name == "ID":
        print(f"Столбец {set_name} нельзя изменить.")
        return table_data
    elif where_name == "ID":
        for key in list(table_data.keys()):
            if int(key) == where_value:
                print(f"Запись с ID={key} в таблице успешно обновлена.")
                table_data[key][set_name] = set_value
        return table_data
    else:
        ids_to_update = []
        for key in list(table_data.keys()):
            if table_data[key][where_name] == where_value:
                ids_to_update.append(key)
        for key in ids_to_update:
            print(f"Запись с ID={key} в таблице успешно обновлена.")
            table_data[key][set_name] = set_value
        return table_data


def delete(table_data, where_clause):
    """
    Удаляет записи удовлетворяющие условию where_clause
    """
    col_name = list(where_clause.keys())[0]
    col_value = where_clause[col_name]
    if col_name == "ID":
        for key in list(table_data.keys()):
            if int(key) == col_value:
                print(f"Запись с ID={key} в таблице успешно удалена.")
                del table_data[key]
        return table_data
    else:
        ids_to_delete = []
        for key in list(table_data.keys()):
            if table_data[key][col_name] == col_value:
                ids_to_delete.append(key)
        for key in ids_to_delete:
            print(f"Запись с ID={key} в таблице успешно удалена.")
            del table_data[key]
        return table_data


def list_tables(metadata):
    for table_name in list(metadata.keys()):
        print(f"- {table_name}")
    return metadata


def drop_table(metadata, table_name):
    if table_name not in list(metadata.keys()):
        print(f"Ошибка: Таблица '{table_name}' не существует.")
        return metadata
    else:
        print(f"Таблица {table_name} успешно удалена.")
        metadata.pop(table_name)
        os.remove(TABLE_DATA_DIR + "/" + table_name + ".json")
        return metadata


def print_table(metadata, table_name, selected_data=None):
    output_table = PrettyTable()
    table_path = TABLE_DATA_DIR + "/" + table_name + ".json"
    if table_name not in list(metadata.keys()):
        print(f"Ошибка: Таблица '{table_name}' не существует.")
    else:
        columns = [col.split(sep=":")[0] for col in list(metadata[table_name].keys())]
        output_table.field_names = columns
        if not selected_data:
            selected_data = utils.load_table_data(table_path)
        for id in list(selected_data.keys()):
            row = [id]
            for column in columns:
                if column != "ID":
                    row.append(selected_data[id][column])
            output_table.add_row(row)
        print(output_table)
