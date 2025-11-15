from datetime import datetime, timedelta
import os
log_file = os.path.abspath("shell.log")

def log(command, res):
    """
    Выполняет логирование и записывает информацию в файл shell.log
    :param command: команда, которую ввёл пользователь
    :param res: её результат (успех / ошибка)
    :return: ничего
    """
    try:
        with open(log_file, "a") as file:
            time = datetime.now()
            real_time = time.replace(microsecond=0)
            if time.microsecond >= 500000:
                real_time += timedelta(seconds=1)
            if res is None:
                file.write(f"{real_time} - [INFO] - {command}\n")
            else:
                file.write(f"{real_time} - [ERROR] - {res}\n")
    except Exception as e:
        print(f"ошибка : {e}")
