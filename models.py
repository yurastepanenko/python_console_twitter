from datetime import datetime

DATA_BASE = 'twitter.json'

main_menu_list = {'1': 'Зарегистрироваться',
                  '2': 'Залогиниться',
                  '0': 'Выход из программы', }

user_menu_actions = {
                     '1': 'Посмотреть свои твиты',
                     '2': 'Создать твит',
                     '3': 'Работа с определенным твитом',
                     '4': 'Посмотреть другие аккаунты',
                     '0': 'Разлогиниться',
                    }

user_menu_twit_actions = {
                     '1': 'Обновить твит',
                     '2': 'Удалить твит',
                     '3': 'Получить среднюю оценку твита',
                     '0': 'Назад',
                    }


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
        # Вынесено локально чтобы не было зацикливания
        from presenter import write_database
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