import os
import typer
from src.paths import convert_path

def reg_cd_command(app: typer.Typer):
    """
    регистрирует команду cd в приложении
    :param app: typer приложение
    :return: ничего
    """
    @app.command(help="Перейти в другой каталог")
    def cd(path: str = typer.Argument(".", help="Путь к каталогу")):
        """
        Перемещает пользователя в другой каталог
        :param path: путь к до каталога
        :return: None / ошибка
        """
        try:
            path = convert_path(path)
            os.chdir(path)
        except Exception as e:
            print(f"cd: ошибка {e}")
            return e
