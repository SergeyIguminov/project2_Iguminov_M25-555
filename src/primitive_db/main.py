#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.primitive_db import engine


def main():
    welcome()
    engine.run()


if __name__ == "__main__":
    main()


def welcome():
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    # user_input = prompt.string("Введите команду: ")
    # try:
    #    if user_input == "exit":
    #        print("Выход из программы...")
    #    elif user_input == "help":
    #        print("<command> exit - выйти из программы")
    #        print("<command> help - справочная информация")
    #    else:
    #        print(f"Неизвестная команда: {user_input}")
    #
    # except (KeyboardInterrupt, EOFError):
    #    print("\nВыход из программы...")
