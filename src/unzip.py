import zipfile
import typer
import os

def reg_unzip_command(app: typer.Typer):
    @app.command()
    def unzip(archive: str = typer.Argument()):
        """
        Распаковывает zip архив
        :param archive: название архива, который надо распаковать
        :return: результат работы (None / error)
        """
        try:
            if not os.path.exists(archive):
                raise Exception("Нет такого архива")
            with zipfile.ZipFile(archive, "r") as zip:
                zip.extractall(".")
        except Exception as e:
            print(f"unzip : ошибка {e}")
            return e
