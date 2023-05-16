from models import user_menu_actions, \
    User, \
    user_menu_twit_actions, \
    accounts_menu, accounts_menu_detail, \
    accounts_menu_detail_actions, \
    UserSerializer, \
    DATA_BASE, \
    AVAILABLE_RATING
import json
import os


def show_menu(menu_list):
    """
    ф-ия , которая отображает основное меню
    @menu_list - словарь, который будем отображать
    """
    for key, value in menu_list.items():
        print(key, value)


def data_exists(excluded_arg):
    """
    функция для обработки ошибок
    :param excluded_arg:
    :param action: декорируемая функция
    :return: выполнение функции или возврат ошибки
    """

    def decorator(action):
        def wrapper(*args, **kwargs):
            if excluded_arg not in args:
                return action(*args, **kwargs)

        return wrapper

    return decorator

    # def wrapper(*args, **kwargs):
    #     if args[1] is not None:
    #         action(*args, **kwargs)
    #
    # return wrapper


def registration(db):
    """
    функция которая проверяет наличие логина в базе и при его отсутствиии - регистрирует пользователя
    :param db: наша база данных
    :return: возвращает "обновленную базу"
    """
    login_name = input("Введите ваш логин: ")
    password = input("Введите ваш пароль: ")

    if login_name not in [user["login"] for user in db]:
        user = User(login_name, password)
        db.append(UserSerializer.serialize(user))
        print(f"Регистрация прошла успешно! зарегистрирован пользователь: {login_name}")
    else:
        print(f"Пользователь {login_name} уже существует! повторите попытку!")

    return db


def login(db):
    """
    Функция, которая позволяет пользователю залогиниться
    :param db: наша база данных
    :return: возвращает нашего пользователя (объект)
    """
    login_name = input("Введите ваш логин: ")
    password = input("Введите ваш пароль: ")

    # ищем пользователя в базе данных
    for user_data in db:
        if user_data["login"] == login_name and user_data["password"] == password:
            return user_data

    print("Некорректный логин или пароль:(")
    return None


def process_menu_for_single_twit(current_user, db):
    """
    функция для работы с пунктом меню "работа с 1 твитом"
    :param current_user: текущий пользователь
    :param db: наша база данных
    :return: ничего не возвращает
    """
    count_twits = current_user.count_tweets()
    # раоботаем с данным пунктом меню только если есть твиты
    if count_twits:
        current_user.show_all_tweets()
        twit_number = get_twit_number(db, current_user)

        #  работа с определнным своим твитом
        if twit_number is not None:
            work_with_single_twit(db, current_user, twit_number)
        else:
            print("Вы выбрали несуществующий номер твита!\n")
    else:
        print("У вас еще нет твитов!Работа с данным пунктом меню невозможна!\n")


@data_exists("current_user")
def user_actions(db, current_user):
    """
    функция которая отображает возможные действия пользоваля и содержит работу с ними
    :param db: база данных
    :param current_user: текущий пользователь
    :return: ничего не возвращает
    """
    current_user = UserSerializer.deserialize(current_user)
    while True:
        show_menu(user_menu_actions)
        choice = input("Выберите один из пунктов меню\n")
        if choice == '1':
            #  посмотреть все свои твиты
            current_user.show_all_tweets()

        elif choice == '2':
            #  создать новый твит
            current_user.create_new_tweet()
            write_database(db)

        elif choice == '3':
            process_menu_for_single_twit(current_user, db)

        elif choice == '4':
            #  Работа с другими аккаунтами
            view_other_accounts(db, current_user)

        elif choice == '0':
            # выход в прошло меню
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
        print(f"Выбранный номер твита - {twit_number + 1}\n")
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


def get_all_users(db):
    """
    Функция для вывода всех пользователей и их нумерации.
    :param db: база данных пользователей
    """
    if not db:
        print("Нет зарегистрированных пользователей.")
        return

    print("Список пользователей:")
    for num, user_data in enumerate(db, 1):
        user = UserSerializer.deserialize(user_data)
        print(f"Номер пользователя: {num}")
        print(f"Логин: {user.login}")
        print("---")


def get_user(db, user_number):
    """
    Функция для выбора пользователя из базы данных по номеру.
    :param db: база данных пользователей
    :param user_number: номер пользователя
    :return: объект пользователя (User) или None, если номер некорректный
    """
    if user_number.isdigit():
        user_number = int(user_number)
        if user_number < 1 or user_number > len(db):
            print("Некорректный номер пользователя.")
            return None

    user_data = db[user_number - 1]
    user = UserSerializer.deserialize(user_data)
    return user


def rate_entry(custom_user, twit_number, db):
    """
    функция для оценки записи (твита).
    @custom_user: Объект пользователя.
    @twit_number: Номер твита в базе данных.
    @db: База данных твитов.
    @:return ничего не возвращает
    """
    while True:
        rating = input("Поставьте оценку от 1 до 5: ")
        if rating.isdigit() and int(rating) in AVAILABLE_RATING:
            twit = custom_user.show_single_tweet(twit_number)

            if twit:
                custom_user.add_rating_to_tweet(twit_number, rating)
                write_database(db)
                break
        else:
            print("Необходимо использовать для оценки значения от 1 до 5")


def add_comment_to_twit(custom_user, twit_number, db):
    """
       функция для добавления комментария.
       @custom_user: Объект пользователя.
       @twit_number: Номер твита в базе данных.
       @db: База данных твитов.
       @:return ничего не возвращает
       """
    comment = input("Введите комментарий: ")
    twit = custom_user.show_single_tweet(twit_number)

    if twit:
        custom_user.add_comment_to_tweet(twit_number, comment)
        write_database(db)


def work_with_other_twit(db, custom_user, twit_number):
    """
    функция для работы с чужим твитом
    :param db: база данных
    :param custom_user: владелец твита
    :param twit_number: твит
    :return: ничего не возвращает
    """
    while True:
        choice = input("Выберите действие:\n")
        if choice == '1':
            # добавить комментарий
            add_comment_to_twit(custom_user, twit_number, db)

        elif choice == '2':
            # Посмотреть все комментарии
            custom_user.show_comments(twit_number)

        elif choice == '3':
            # оценить и добавить комментарий
            rate_entry(custom_user, twit_number, db)
            add_comment_to_twit(custom_user, twit_number, db)

        elif choice == '0':
            break

        else:
            print("Нет такого пункта меню или он в разработке. Повторите свой выбор!")


def work_with_other_account(db, custom_user):
    """
    функция для работы с конкретным аккаунтом
    :param db: база данных
    :param custom_user: пользователь для просмотра
    :return: ничего не возвращает
    """
    while True:
        choice = input("Выберите действие:\n")
        if choice == '1':
            custom_user.show_all_tweets()

        elif choice == '2':
            custom_user.show_all_tweets()
            twit_number = get_twit_number(db, custom_user)
            custom_user.show_single_tweet(twit_number)
            show_menu(accounts_menu_detail_actions)
            work_with_other_twit(db, custom_user, twit_number)

        elif choice == '0':
            break


def view_other_accounts(db, current_user):
    """
    функция для работы с другими пользователями
    :param db: база данных
    :param current_user: текущий пользователь
    :return: ничего не возвращает
    """
    while True:
        show_menu(accounts_menu)
        choice = input("Выберите один из пунктов (введите число):\n")
        if choice == "1":
            get_all_users(db)

        elif choice == "2":
            user_number = input("Введите номер пользователя, которого будем просматривать\n")
            custom_user = get_user(db, user_number)
            show_menu(accounts_menu_detail)
            work_with_other_account(db, custom_user)

        elif choice == "0":
            break


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
