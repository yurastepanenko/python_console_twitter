from models import user_menu_actions, User
import json
import os
from models import DATA_BASE


def show_menu(menu_list):
    """
    ф-ия , которая отображает основное меню
    @menu_list - словарь, который будем отображать
    """
    for key, value in menu_list.items():
        print(key, value)


def data_exists(action):
    """
    функция для обработки ошибок
    :param action: декорируемая функция
    :return: выполнение функции или возврат ошибки
    """
    def wrapper(*args, **kwargs):
        if args[1] is not None:
            action(*args, **kwargs)
    return wrapper


def registration(db):
    """
    функция которая проверяет наличие логина в базе и при его отсутствиии - регистрирует пользователя
    :param db: наша база данных
    :return: возвращает "обновленную базу"
    """
    login = input("Введите ваш логин: ")
    password = input("Введите ваш пароль: ")

    if login not in [user["login"] for user in db]:
        user = User(login, password)
        db.append(user.to_dict())
        print(f"Регистрация прошла успешно! зарегистрирован пользователь: {login}")
        print(id(user))
    else:
        print(f"Пользователь {login} уже существует! повторите попытку!")

    return db


def login(db):
    """
    Функция, которая позволяет пользователю залогиниться
    :param db: наша база данных
    :return: возвращает нашего пользователя (объект)
    """
    login = input("Введите ваш логин: ")
    password = input("Введите ваш пароль: ")

    # Иначе ищем пользователя в базе данных
    for user_data in db:
        if user_data["login"] == login and user_data["password"] == password:
            return user_data

    print("Некорректный логин или пароль:(")
    return None


@data_exists
def user_actions(db, current_user):
    current_user = User.from_dict(current_user)
    while True:
        show_menu(user_menu_actions)
        choice = input("Выберите один из пунктов меню\n")
        if choice == '1':
            current_user.show_all_tweets()

        elif choice == '2':
            current_user.create_new_tweet(db)
            update_user_database(db, current_user)

            # db.append(current_user.to_dict())
            write_database(db)

        elif choice == '3':
            work_with_single_twit(db, current_user)

        elif choice == '4':
            view_other_accounts(db, current_user)

        elif choice == '0':
            break

        else:
            print("Такого пункта меню не существует или он в разработке:) Попробуйте еще раз!")


def work_with_single_twit(db, current_user):
    print("work_with_single_twit")


def view_other_accounts(db, current_user):
    print("view_other_accounts")

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


def update_user_database(db, user):
    """
    Функция для обновления базы данных пользователей после создания твита.
    :param db: база данных пользователей
    :param user: объект пользователя
    """
    for user_data in db:
        if user_data["login"] == user.login:
            # Обновить список твитов пользователя
            user_data["twits"].append(user.twits[-1])
            write_database(db)
            break
