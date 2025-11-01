import typer

def reg_cat_command(app: typer.Typer):
    @app.command(help="Выводит содержимое файла в консоль")
    def cat(file: str = typer.Argument(help="Название файла вместе с расширением")):
        """
        Выводит содержимое файла
        :param file: файл, содержимое которого хотим увидеть
        :return: возвращает None / ошибку и выводит данные из файла
        """
        try:
            f = open(file)
            print(f.read())
            f.close()
        except Exception as e:
            print(f"cat : ошибка {e}")
            return e
