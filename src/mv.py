import typer
import os
import shutil

def reg_mv_command(app: typer.Typer):
    @app.command()
    def mv(source: list[str] = typer.Argument(), destination: str = typer.Argument()):
        """
        Перемещает файл или каталог из одного места в другое
        :param source: файл, который надо переместить
        :param destination: место, куда хотим переместить (место назначения)
        :return: None / error
        """
        try:
            if len(source) == 1:
                shutil.move(source[0], destination)
            elif len(source) > 1:
                for file in source:
                    file = os.path.basename(file)
                    path = os.path.join(destination, file)
                    shutil.move(file, path)
        except Exception as e:
            print(f"mv : ошибка {e}")
            return e
