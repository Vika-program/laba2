import tarfile
import typer
import os

def reg_tar_command(app: typer.Typer):
    @app.command()
    def tar(folder: str = typer.Argument(), archive: str = typer.Argument("folder")):
        """
        Функция создаёт архив формата tar из каталога
        :param folder: исходный каталог
        :param archive: название архива, который будет создан (по умолчанию folder)
        :return: результат работы (None / error)
        """
        try:
            if not os.path.exists(folder):
                raise Exception("Нет такого каталога")
            with tarfile.open(archive, "w:gz") as tar:
                tar.add(folder)
        except Exception as e:
            print(f"tar : ошибка {e}")
            return e
