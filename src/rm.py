import typer
import os
import shutil

def reg_rm_command(app: typer.Typer):
    """
    регистрирует команду rm в приложении
    :param app: typer приложение
    :return: None / error
    """
    @app.command()
    def rm(flag: bool = typer.Option(False, "-r"), files: list[str] = typer.Argument()):
        print(flag)
        print(files)
        """
        Команда удаляет файл или каталог
        :param flag: флаг рекурсивного удаления
        :param files: то, что нужно удалить
        :return: возвращает результат работы функции
        """
        try:
            for file in files:
                if not os.path.exists(file):
                    raise Exception(f"файл или каталог {file} не существует")
                if os.path.isfile(file):
                    os.remove(file)
                elif os.path.isdir(file) and flag:
                    print(os.path.dirname(os.getcwd()), file in os.path.dirname(os.getcwd()))
                    if file == '/' or file in os.path.dirname(os.getcwd()):
                        raise Exception("Вы не можете удалить корневой каталог или родительский!")
                    answer = input(f"Вы хотите удалить каталог {file}? "
                        f"Напишите y, если согласны, n - если отказываетесь>>")
                    if answer == "y":
                        shutil.rmtree(file)
                elif os.path.isdir(file) and not flag:
                    raise Exception("Нельзя удалить каталог без флага -r")
        except Exception as e:
            print(f"rm : ошибка : {e}")
            return e
