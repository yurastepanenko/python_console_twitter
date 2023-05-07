import json
import os
from models import DATA_BASE


def database_initialization():
    """
    функция создаст условную базу данных, если та не существовала
    :return:
    """
    if not os.path.exists(DATA_BASE):
        with open(DATA_BASE, "a") as f:
            f.write(json.dumps([]))


def read_database():
    """
        функция вычитывает базу данных
        :return: возвращает результат в формате json
        """
    with open(DATA_BASE, "r") as f:
        return json.loads(f.read())


def write_database(data):
    """
    функция записывает в базу данных
    :return: ничего не возвращает
    """
    with open(DATA_BASE, "w") as f:
        f.write(json.dumps(data))