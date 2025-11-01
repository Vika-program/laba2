import typer
import shlex
import os
from src.ls import reg_ls_command
from src.cd import reg_cd_command
from src.cat import reg_cat_command
from src.cp import reg_cp_command
from src.log import log
from src.mv import reg_mv_command
from src.rm import reg_rm_command
from src.zip import reg_zip_command
from src.unzip import reg_unzip_command
from src.tar import reg_tar_command
from src.untar import reg_untar_command
from src.grep import reg_grep_command
from src.history import log_history, reg_history_command

app = typer.Typer(name = "Моя командная строка)")
reg_ls_command(app)
reg_cd_command(app)
reg_cat_command(app)
reg_cp_command(app)
reg_mv_command(app)
reg_rm_command(app)
reg_zip_command(app)
reg_unzip_command(app)
reg_tar_command(app)
reg_untar_command(app)
reg_grep_command(app)
reg_history_command(app)

def parsing(inp):
    try:
        inp = shlex.split(inp)
        if not inp:
            return None
        return inp
    except Exception:
        print("Ошибка парсинга")
        return None

@app.command()
def shell():
    while True:
        cur_dir = os.getcwd()
        inp = input(f"{cur_dir}>>").strip()
        if inp == "exit":
            break
        res = parsing(inp)
        if res is None:
            continue
        try:
            output = app(res, standalone_mode=False)
            log(inp, output)
            log_history(inp)
        except Exception as e:
            print(f"ошибка : {e}")
            pass

if __name__ == "__main__":
    app(['shell'])
