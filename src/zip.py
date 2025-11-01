import typer
import os
import zipfile

def reg_zip_command(app: typer.Typer):
    @app.command()
    def zip(folder: str = typer.Argument(), archive: str = typer.Argument("folder")):
        """
        Функция создаёт архив zip из каталога
        :param folder: исходный каталог
        :param archive: название архива, который будет создан (по умолчанию folder)
        :return: результат работы (None / error)
        """
        try:
            if not os.path.exists(folder):
                raise Exception("Нет такого каталога")
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zip:
                parent_dir = os.path.dirname(folder)
                for root_folder, dirs, files in os.walk(folder):
                    for file in files:
                        path = os.path.join(root_folder, file)
                        name_archive = os.path.relpath(path, parent_dir)
                        zip.write(path, name_archive)
        except Exception as e:
            print(f"zip : ошибка {e}")
            return e
