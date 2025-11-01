import typer

def log_history(inp):
    """
    Записывает ввод пользователя в файл .history
    :param inp: ввод пользователя
    :return: ничего
    """
    with open(".history", "r") as file:
        num = 1
        for line in file:
            num += 1
    with open(".history", "a") as file:
        file.write(f"{num} : {inp}\n")

def reg_history_command(app: typer.Typer):
    @app.command()
    def history(n: str = typer.Argument(5)):
        """
        Выводит n строк и файла .history
        :param n: количество последних строк, которые нужно вывести
        :return: печатает эти строки
        """
        n = int(n)
        with open('.history', 'r') as file:
            lines = file.readlines()
            n = min(len(lines), n)
            for i in range(len(lines) - n, len(lines)):
                print(lines[i].rstrip())
