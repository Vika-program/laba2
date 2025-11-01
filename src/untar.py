import tarfile
import typer
import os

def reg_untar_command(app: typer.Typer):
    @app.command()
    def untar(archive: str = typer.Argument()):
        """
        Распаковывает tar архив
        :param archive: название архива, который надо распаковать
        :return: результат работы (None / error)
        """
        try:
            if not os.path.exists(archive):
                raise Exception("Нет такого архива")
            with tarfile.open(archive, "r:gz") as tar:
                tar.extractall('.')
        except Exception as e:
            print(f"untar : ошибка {e}")
            return e
