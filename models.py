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

    # def __new__(cls, login, password):
    #     # Проверяем, есть ли пользователь с таким логином в кэше
    #     if login in cls.__users_cache:
    #         # Если есть, возвращаем уже существующий экземпляр
    #         return cls.__users_cache[login]
    #
    #     # Создаем новый экземпляр
    #     instance = super().__new__(cls)
    #     cls.__users_cache[login] = instance
    #     return instance

    def __init__(self, login, password, twits=None):
        self.__login = login
        self.__password = password
        self.__twits = twits or []

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

    @classmethod
    def from_dict(cls, user_dict):
        """
        Метод создает экземпляр класса User на основе словаря
        :param user_dict: словарь с данными пользователя
        :return: экземпляр класса User
        """
        login = user_dict.get('login')
        password = user_dict.get('password')
        twits = user_dict.get('twits')
        return cls(login, password, twits)



    def show_all_tweets(self):
        """
        Метод для просмотра всех твитов пользователя.
        """
        if self.__twits:
            print("Список твитов:")
            for num, twit_dict in enumerate(self.__twits, 1):
                twit = TwittSerializer.deserialize(twit_dict)
                print(f"Номер твита: {num}")
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
        self.__twits.append(TwittSerializer.serialize(twit))

    def count_tweets(self):
        """
        Метод для подсчета количества твитов пользователя.
        :return: количество твитов
        """
        return len(self.__twits)

    def update_tweet(self, twit_number):
        """
        Метод для обновления твита пользователя.
        :param db: база данных
        :param twit_number: номер твита для обновления
        :return: ничего не возвращает
        """

        twit_dict = self.__twits[twit_number]
        twit = TwittSerializer.deserialize(twit_dict)

        new_title = input("Введите новый заголовок твита: ")
        new_text = input("Введите новый текст твита: ")

        # Обновляем данные твита
        twit.title = new_title
        twit.text = new_text

        # Преобразуем обновленный твит в словарь и заменяем его в списке твитов пользователя
        self.__twits[twit_number] = TwittSerializer.serialize(twit)

        print("Твит успешно обновлен.")

    def delete_tweet(self, twit_number):
        """
        Метод для обновления твита пользователя.
        :param db: база данных
        :param twit_number: номер твита для удаления
        :return: ничего не возвращает
        """
        del self.__twits[twit_number]


class Twitt:
    def __init__(self, title, text, time):
        self.title = title
        self.text = text
        self.ratings = []
        self.comments = []
        self.time = time


class TwittSerializer:
    @staticmethod
    def serialize(twitt):
        """
        Метод преобразует объект твита в словарь.
        :param twitt: объект твита
        :return: словарь с данными твита
        """
        return {
            'title': twitt.title,
            'text': twitt.text,
            'ratings': twitt.ratings,
            'comments': twitt.comments,
            'time': twitt.time.isoformat()
        }

    @staticmethod
    def deserialize(twit_dict):
        """
        Метод создает экземпляр класса Twitt из словаря.
        :param twit_dict: словарь с данными твита
        :return: экземпляр класса Twitt
        """
        return Twitt(
            title=twit_dict["title"],
            text=twit_dict["text"],
            time=datetime.fromisoformat(twit_dict["time"])
        )
