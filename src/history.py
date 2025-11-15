import typer
import os
history_file = os.path.abspath(".history")

def log_history(inp):
    """
    Записывает ввод пользователя в файл .history
    :param inp: ввод пользователя
    :return: ничего
    """
    try:
        with open(history_file, "r") as file:
            num = 1
            for line in file:
                num += 1
        with open(history_file, "a") as file:
            file.write(f"{num} : {inp}\n")
    except Exception as e:
        print(f"ошибка : {e}")

def reg_history_command(app: typer.Typer):

    @app.command()
    def history(n: int = typer.Argument(5)):
        """
        Выводит n строк и файла .history
        :param n: количество последних строк, которые нужно вывести
        :return: печатает эти строки
            """
        try:
            with open(history_file, 'r') as file:
                lines = file.readlines()
                n = min(len(lines), n)
                for i in range(len(lines) - n, len(lines)):
                    print(lines[i].rstrip())
        except Exception as e:
            print(f"ошибка : {e}")
