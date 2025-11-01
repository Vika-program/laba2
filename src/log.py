from datetime import datetime, timedelta

def log(command, res):
    """
    Выполняет логирование и записывает информацию в файл shell.log
    :param command: команда, которую ввёл пользователь
    :param res: её результат (успех / ошибка)
    :return: ничего
    """
    with open("shell.log", "a") as file:
        time = datetime.now()
        real_time = time.replace(microsecond=0)
        if time.microsecond >= 500000:
            real_time += timedelta(seconds=1)
        if res is None:
            file.write(f"{real_time} - [INFO] - {command}\n")
        else:
            file.write(f"{real_time} - [ERROR] - {res}\n")
