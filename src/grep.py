import typer
import re
import os
import fnmatch

def search_file(pattern, path, flag_i):
    """
    Ищет совпадения с шаблоном в файле
    :param pattern: шаблон
    :param path: путь к файлу
    :param flag_i: флаг для игнорирования регистра
    :return: совпадения с шаблоном
    """
    with open(path, 'r') as f:
        lines = f.readlines()
        for num, line in enumerate(lines, 1):
            if flag_i:
                pattern = pattern.lower()
                line = line.lower()
            if os.path.isfile(path):
                for match in re.finditer(pattern, line):
                    start = max(0, match.start() - 10)
                    end = min(len(line), match.end() + 10)
                    print(path, num, line[start:end])


def search_dir(files, pattern, root, flag_i):
    """
    Ищет совпадения в каталоге
    :param files: каталог / каталоги
    :param pattern: шаблон
    :param root: родительский каталог
    :param flag_i: флаг для игнорирования регистра
    :return: возвращает совпадения с шаблоном
    """
    for file in files:
        if pattern.startswith('*.'):
            if fnmatch.fnmatch(file, pattern):
                print(file)
        else:
            path = os.path.join(root, file)
            if os.path.isfile(path):
                search_file(pattern, path, flag_i)


def reg_grep_command(app: typer.Typer):
    @app.command()
    def grep(flag_r: bool = typer.Option(False, "-r"), flag_i: bool = typer.Option(False, "-i"),
             pattern: str =  typer.Argument(), items: list[str] = typer.Argument()):
        """
        Функция ищет элементы, подходящие под шаблон
        :param flag_r: флаг для рекурсии
        :param flag_i: флаг для игнорирования регистра
        :param pattern: шаблон
        :param items: то, где будем искать
        :return: None / error / строки, подходящие под шаблон
        """
        try:
            for item in items:
                if os.path.isfile(item):
                    search_file(pattern, item, flag_i)
                else:
                    if flag_r:
                        for root, dirs, files in os.walk(item):
                            search_dir(files, pattern, root, flag_i)
                    else:
                        files = os.listdir(item)
                        search_dir(files, pattern, item, flag_i)
        except Exception as e:
            print(f"grep : ошибка {e}")
            return e
