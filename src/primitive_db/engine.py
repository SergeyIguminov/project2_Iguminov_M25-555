import shlex

import prompt

import src.primitive_db.parser as parser
from src.primitive_db import core, utils

METADATA_PATH = "src/db_meta.json"
TABLE_DATA_DIR = "data"


def run():
    while True:
        metadata = utils.load_metadata(METADATA_PATH)
        user_input = prompt.string("Введите команду: ")
        args = shlex.split(user_input)
        if not args:
            continue
        match args[0]:
            case "create_table":
                metadata = core.create_table(metadata, args[1], args[2:])
                utils.save_metadata(METADATA_PATH, metadata)
            case "drop_table":
                metadata = core.drop_table(metadata, args[1])
                utils.save_metadata(METADATA_PATH, metadata)
            case "list_tables":
                core.list_tables(metadata)

            case "insert":
                if len(args) > 4:
                    if args[1] == "into" and args[3] == "values":
                        table_name = args[2]
                        table_values = [
                            val.replace("(", "").replace(")", "").replace(",", "")
                            for val in args[4:]
                        ]
                        if len(table_values) == len(metadata[table_name].keys()) - 1:
                            table_values = parser.parse_values(
                                table_values, list(metadata[table_name].keys())[1:]
                            )
                            core.insert(metadata, table_name, table_values)
                        else:
                            print(
                                "Число переменных не соответствует "
                                "числу столбцов. Попробуйте снова."
                            )
                    else:
                        print("Некорректный синтаксис. Попробуйте снова.")
                else:
                    print("Некорректный синтаксис. Попробуйте снова.")
            case "select":
                if len(args) == 7:
                    if args[1] == "from" and args[3] == "where" and args[5] == "=":
                        table_name = args[2]
                        table_path = TABLE_DATA_DIR + "/" + table_name + ".json"
                        if table_name in list(metadata.keys()):
                            table_data = utils.load_table_data(table_path)
                        else:
                            print(f"Ошибка: Таблица '{table_name}' не существует.")
                            continue
                        col_names = [
                            col.split(sep=":")[0]
                            for col in list(metadata[table_name].keys())
                        ]
                        if args[4] not in col_names:
                            print(f"Столбца {args[4]} в таблице {table_name} нет.")
                        else:
                            col_index = col_names.index(args[4])
                            preferred_type = list(metadata[table_name].keys())[
                                col_index
                            ].split(sep=":")[1]
                            clause, success = parser.parse(
                                args[4] + "=" + args[6], preferred_type
                            )
                            if success:
                                select_data = core.select(table_data, clause)
                                core.print_table(metadata, table_name, select_data)
                            else:
                                print(
                                    f"Значение {args[6]} нельзя использовать "
                                    f"для столбца типа {preferred_type}."
                                )
                    else:
                        print("Некорректный синтаксис. Попробуйте снова.")
                elif len(args) == 3:
                    table_name = args[2]
                    table_path = TABLE_DATA_DIR + "/" + table_name + ".json"
                    if table_name in list(metadata.keys()):
                        table_data = utils.load_table_data(table_path)
                    else:
                        print(f"Ошибка: Таблица '{table_name}' не существует.")
                        continue
                    core.print_table(metadata, table_name)
                else:
                    print("Некорректный синтаксис. Попробуйте снова.")
            case "update":
                if len(args) == 10:
                    if (
                        args[2] == "set"
                        and args[4] == "="
                        and args[6] == "where"
                        and args[8] == "="
                    ):
                        table_name = args[1]
                        table_path = TABLE_DATA_DIR + "/" + table_name + ".json"
                        if table_name in list(metadata.keys()):
                            table_data = utils.load_table_data(table_path)
                        else:
                            print(f"Ошибка: Таблица '{table_name}' не существует.")
                            continue
                        col_names = [
                            col.split(sep=":")[0]
                            for col in list(metadata[table_name].keys())
                        ]
                        if args[3] not in col_names:
                            print(f"Столбца {args[3]} в таблице {table_name} нет.")
                        elif args[7] not in col_names:
                            print(f"Столбца {args[7]} в таблице {table_name} нет.")
                        else:

                            set_index = col_names.index(args[3])
                            preferred_set_type = list(metadata[table_name].keys())[
                                set_index
                            ].split(sep=":")[1]
                            set_clause, set_success = parser.parse(
                                args[3] + "=" + args[5], preferred_set_type
                            )
                            where_index = col_names.index(args[7])
                            preferred_where_type = list(metadata[table_name].keys())[
                                where_index
                            ].split(sep=":")[1]
                            where_clause, where_success = parser.parse(
                                args[7] + "=" + args[9], preferred_where_type
                            )
                            if not set_success:
                                print(
                                    f"Значение {args[3]} нельзя использовать "
                                    f"для столбца типа {preferred_set_type}."
                                )
                            elif not where_success:
                                print(
                                    f"Значение {args[7]} нельзя использовать "
                                    f"для столбца типа {preferred_where_type}."
                                )
                            else:
                                new_table_data = core.update(
                                    table_data, set_clause, where_clause
                                )
                                if new_table_data:
                                    table_data = new_table_data
                                utils.save_table_data(table_path, table_data)
                    else:
                        print("Некорректный синтаксис. Попробуйте снова.")
                else:
                    print("Некорректный синтаксис. Попробуйте снова.")
            case "delete":
                if len(args) == 7:
                    if args[1] == "from" and args[3] == "where" and args[5] == "=":
                        table_name = args[2]
                        table_path = TABLE_DATA_DIR + "/" + table_name + ".json"
                        if table_name in list(metadata.keys()):
                            table_data = utils.load_table_data(table_path)
                        else:
                            print(f"Ошибка: Таблица '{table_name}' не существует.")
                            continue
                        col_names = [
                            col.split(sep=":")[0]
                            for col in list(metadata[table_name].keys())
                        ]
                        if args[4] not in col_names:
                            print(f"Столбца {args[4]} в таблице {table_name} нет.")
                        else:
                            col_index = col_names.index(args[4])
                            preferred_type = list(metadata[table_name].keys())[
                                col_index
                            ].split(sep=":")[1]
                            clause, success = parser.parse(
                                args[4] + "=" + args[6], preferred_type
                            )
                            if success:
                                new_table_data = core.delete(table_data, clause)
                                if new_table_data:
                                    table_data = new_table_data
                                utils.save_table_data(table_path, table_data)
                            else:
                                print(
                                    f"Значение {args[6]} нельзя использовать "
                                    f"для столбца типа {preferred_type}."
                                )
                    else:
                        print("Некорректный синтаксис. Попробуйте снова.")
                else:
                    print("Некорректный синтаксис. Попробуйте снова.")

            case "help":
                print_help()
            case "exit":
                print("Выход из программы...")
                break
            case _:
                print(
                    f"Команды '{args[0]}' нет. Попробуйте снова. "
                    f"Команда help - для справки"
                )


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
