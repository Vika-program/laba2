import shutil
import typer
import os

def reg_cp_command(app: typer.Typer):
    """
    регистрирует команду cp в приложении
    :param app: typer приложение
    :return: ничего
    """
    @app.command()
    def cp(flag: bool = typer.Option(False, "-r"),
           files: list[str] = typer.Argument(),
           destination: str = typer.Argument()):
        """
        Команда копирует информацию из источника в файл или папку назначения
        :param flag: флаг рекурсивного копирования
        :param files: источник, из которого копируется информация
        :param destination: место назначения
        :return: возвращает None / ошибку
        """
        try:
            if flag and not os.path.isdir(files[0]):
                flag = False
            if not os.path.exists(destination) and len(files) > 1:
                os.mkdir(destination)
            if not flag:
                if len(files) > 1:
                    if not os.path.isdir(destination):
                        raise NotADirectoryError(f"{destination} Не каталог")
                    for file in files:
                        shutil.copy(file, destination)
                elif len(files) == 1:
                    shutil.copy(files[0], destination)
            else:
                if os.path.exists(destination):
                    shutil.rmtree(destination)
                shutil.copytree(files[0], destination)
        except Exception as e:
            print(f"cp : ошибка {e}")
            return e
