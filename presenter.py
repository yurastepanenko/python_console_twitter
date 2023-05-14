from models import user_menu_actions, User, user_menu_twit_actions
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
            # update_user_database(db, current_user)
            write_database(db)

        elif choice == '3':
            current_user.show_all_tweets()
            twit_number = get_twit_number(db, current_user)
            work_with_single_twit(db, current_user, twit_number)

        elif choice == '4':
            view_other_accounts(db, current_user)

        elif choice == '0':
            break

        else:
            print("Такого пункта меню не существует или он в разработке:) Попробуйте еще раз!")


def get_twit_number(db, current_user):
    """
    Функция, которая позволяет выбрать твит пользователя
    :param current_user: текущий пользователь
    :param db: наша база данных
    :return: возвращает номер твита в базе данных
    """
    twit_number = input("Выберите Номер твита (число)\n")
    if twit_number.isdigit() and 0 <= int(twit_number) <= current_user.count_tweets():
        twit_number = int(twit_number) - 1  # делаем человеческую нумерацию(так как индексы с 0)
        print(f"Выбранный номер твита - {twit_number + 1}")
        return twit_number


def work_with_single_twit(db, current_user, twit_number):
    show_menu(user_menu_twit_actions)
    choice = input("Выберите один из пунктов (введите число):\n")

    if choice == "1":
        current_user.update_tweet(twit_number)
        write_database(db)


    elif choice == "2":
        current_user.delete_tweet(twit_number)
        write_database(db)


    elif choice == "3":
        current_user.get_avg_score(twit_number)





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
