import utils, core
import shlex
import prompt


def run():
    while True:
        metadata = utils.load_metadata()
        user_input = prompt.string("Введите команду: ")
        args = shlex.split(user_input)
        match args[0]:
            case "create_table":
                metadata = core.create_table(metadata, args[1], args[2:])
                utils.save_metadata(metadata)
            case "drop_table":
                metadata = core.drop_table(metadata, args[1])
                utils.save_metadata(metadata)
            case "list_tables":
                print(*metadata["tables"])
            case "help":
                print_help()
            case "exit":
                print("Выход из программы...")
                break


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
