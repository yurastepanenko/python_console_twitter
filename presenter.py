from models import user_menu_actions
from datetime import datetime
from db_presenter import write_database


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
        print(user_data)
        if user_data["login"] == login and user_data["password"] == password:
            # Создаем новый экземпляр пользователя
            # user = User.__new__(User, user_data["login"], user_data["password"])
            user = User.__new__(User, login, password)
            print("Вы успешно авторизовались:)")
            return user

    print("Некорректный логин или пароль:(")
    return None

@data_exists
def user_actions(db, current_user):
    print(db, current_user)
    while True:
        show_menu(user_menu_actions)
        choice = input("Выберите один из пунктов меню\n")
        if choice == '1':
            current_user.show_all_tweets()

        elif choice == '2':
            print(id(current_user))
            current_user.create_new_tweet(db)
            print(db)
            db.append(current_user.to_dict())
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


class User:
    __users_cache = {}

    def __new__(cls, login, password):
        # Проверяем, есть ли пользователь с таким логином в кэше
        if login in cls.__users_cache:
            # Если есть, возвращаем уже существующий экземпляр
            return cls.__users_cache[login]

        # Создаем новый экземпляр
        instance = super().__new__(cls)
        cls.__users_cache[login] = instance
        return instance

    def __init__(self, login, password):
        self.__login = login
        self.__password = password
        self.__twits = []

    @property
    def login(self):
        return self.__login

    @property
    def twits(self):
        return self.__twits

    def check_data(self, login, password):
        if self.__login == login and self.__password == password:
            return True
        else:
            return False

    # def __str__(self):
    #     return self.__login

    def to_dict(self):
        """
        метод привод объект юзера к словарю
        :return: возвращает словарь(сконвертированного юзера)
        """
        return {
            'login': self.__login,
            'password': self.__password,
            'twits': self.__twits
        }

    def show_all_tweets(self):
        """
        Метод для просмотра всех твитов пользователя.
        """
        if self.__twits:
            print("Список твитов:")
            for twit_dict in self.__twits:
                twit = Twitt.from_dict(twit_dict)
                print(f"Заголовок: {twit.title}")
                print(f"Текст: {twit.text}")
                print("---")
        else:
            print("У вас пока нет твитов.")

    def create_new_tweet(self, db):
        """
        Метод для создания нового твита
        """
        title = input("Введите заголовок твита: ")
        text = input("Введите текст твита: ")
        time = datetime.now()
        twit = Twitt(title, text, time)
        self.__twits.append(twit.to_dict())

        for user_data in db:
            if user_data["login"] == self.login:
                # Обновить список твитов пользователя
                user_data["twits"].append(twit.to_dict())
                write_database(db)
                break


class Twitt:
    def __init__(self, title, text, time):
        self.title = title
        self.text = text
        self.ratings = []
        self.comments = []
        self.time = time

    def to_dict(self):
        """
        метод привод объект твита к словарю
        :return: возвращает словарь(сконвертированный твит)
        """
        return {
            'title': self.title,
            'text': self.text,
            'ratings': self.ratings,
            'comments': self.comments,
            'time': self.time.isoformat()
        }

    @classmethod
    def from_dict(cls, twit_dict):
        """
        Метод класса для создания экземпляра твита из словаря.
        :param twit_dict: словарь с данными твита
        :return: экземпляр класса Twitt
        """
        return cls(
            title=twit_dict["title"],
            text=twit_dict["text"],
            time=datetime.fromisoformat(twit_dict["time"])
            )