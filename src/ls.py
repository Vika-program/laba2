import os
import stat
import typer
from datetime import datetime
from src.paths import convert_path


def reg_ls_command(app: typer.Typer):
    """
    регистрирует команду ls в приложении
    :param app: typer приложение
    :return: ничего
    """
    @app.command(help="Вывести информацию о всех файлах в каталоге")
    def ls(flag: bool = typer.Option(False, "-l", help="Показать развернутый вариант"),
           path: str = typer.Argument(".", help="Путь к каталогу")):
        """
        Выводит информацию о всех файлах в каталоге
        :param flag: флаг, позволяющий вывести развёрнутую информациию о файле
        :param path: каталог / путь до него
        :return: возвращает ошибку или ничего не возвращает и выводит информацию о файлах
        """
        try:
            path = convert_path(path)
            files = os.listdir(path)
            if flag:
                for file in files:
                    file_path = os.path.join(path, file)
                    info = os.stat(file_path)
                    time = datetime.fromtimestamp(info.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    size = info.st_size
                    file_mode = os.stat(file_path).st_mode
                    access = stat.filemode(file_mode)
                    print(access, file, size, time)
            else:
                print(*files)
        except Exception as e:
            print(f"ls : ошибка {e}")
            return e
