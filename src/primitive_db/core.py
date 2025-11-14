def create_table(metadata, table_name, columns):
    if "tables" not in metadata:
        metadata["tables"] = {}

    # Проверка существования таблицы в метаданных
    if table_name in metadata["tables"]:
        print(f"Ошибка: Таблица '{table_name}' уже существует")
        return metadata

    # Проверка корректности типов данных
    valid_types = {"int", "str", "bool"}
    for col_name, col_type in columns:
        if col_type not in valid_types:
            print(
                f"Ошибка: Неподдерживаемый тип '{col_type}' для столбца '{col_name}'. Допустимые типы: {', '.join(valid_types)}"
            )
            return metadata

    table_columns = [("ID", "int")] + columns

    metadata["tables"][table_name] = {"columns": table_columns, "data": []}

    print(f"Таблица '{table_name}' успешно создана")
    return metadata


def drop_table(metadata, table_name):
    if table_name in metadata["tables"]:
        del metadata["tables"][table_name]
    else:
        print(f"Ошибка: таблицы {table_name} не существует")
    return metadata
