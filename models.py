from datetime import datetime

# возможные оценки для ретинга
AVAILABLE_RATING = [1, 2, 3, 4, 5]

# название базы данных(наш фал json)
DATA_BASE = 'twitter.json'


class User:
    """
    Класс пользователя базы данных твиттера
    """
    def __init__(self, login, password, twits=[]):
        """
        метод для инициализации нового пользователя
        :param login: Логин пользователя
        :param password: Пароль пользователя
        :param twits:
        """
        self.__login = login
        self.__password = password
        self.__twits = twits

    @property
    def login(self):
        return self.__login

    @property
    def twits(self):
        return self.__twits

    @property
    def password(self):
        return self.__password

    def show_all_tweets(self):
        """
        Метод для просмотра всех твитов пользователя.
        """
        if self.__twits:
            print("Список твитов:")
            for num, twit_dict in enumerate(self.__twits, 1):
                twit = TwittSerializer.deserialize(twit_dict)
                print(f"Номер твита: {num}")
                twit.display_tweet()
        else:
            print("У вас пока нет твитов.")

    def is_valid_tweet_number(self, twit_number):
        """
        Вспомогательный метод для проверки корректности номера твита.
        :param twit_number: номер твита
        :return: True, если номер корректный, False в противном случае
        """
        if twit_number < 0 or twit_number >= len(self.__twits):
            return False
        return True

    def get_single_tweet(self, twit_number):
        """
        Метод для просмотра одного твита.
        :param twit_number: номер твита
        :return ничего не возвращает
        """
        if not self.is_valid_tweet_number(twit_number):
            print("Некорректный номер твита.")
            return

        twit = self.__twits[twit_number]
        twit = TwittSerializer.deserialize(twit)
        # twit = TwittSerializer.serialize(twit)
        return twit

    def create_new_tweet(self):
        """
        Метод для создания нового твита
        """
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

    def delete_tweet(self, twit_number):
        """
        Метод для обновления твита пользователя.
        :param twit_number: номер твита для удаления
        :return: ничего не возвращает
        """
        del self.__twits[twit_number]
        print("Твит успешно удален")

    def add_comment_to_tweet(self, twit_number, comment):
        """
        Метод для добавления комментария к твиту.
        :param twit_number: номер твита
        :param comment: текст комментария
        """
        twit_dict = self.__twits[twit_number]
        twit = TwittSerializer.deserialize(twit_dict)
        twit.comments.append(comment)
        self.__twits[twit_number] = TwittSerializer.serialize(twit)
        print("Комментарий успешно добавлен.")

    def add_rating_to_tweet(self, twit_number, rating):
        """
        Метод для добавления рейтинга к твиту.
        :param twit_number: номер твита
        :param rating: рейтинг
        """
        twit_dict = self.__twits[twit_number]
        twit = TwittSerializer.deserialize(twit_dict)
        twit.ratings.append(int(rating))
        self.__twits[twit_number] = TwittSerializer.serialize(twit)
        print("Рейтинг успешно добавлен.")

    def show_comments(self, twit_number):
        """
        Метод для отображения комментариев к указанному твиту.
        :param twit_number: номер твита
        """
        twit_dict = self.__twits[twit_number]
        twit = TwittSerializer.deserialize(twit_dict)
        comments = twit.comments
        if comments:
            print("Комментарии к твиту №{}:".format(twit_number))
            for comment in comments:
                print(comment)
        else:
            print("У твита №{} нет комментариев.".format(twit_number))

    def update_tweet_in_list(self, updated_twit, twit_number):
        """
        Метод для обновления твита в списке твитов пользователя.
        :param updated_twit: обновленный твит (объект Twitt или словарь)
        :param twit_number: номер твита для обновления
        :return: ничего не возвращает
        """
        if isinstance(updated_twit, dict):
            updated_twit = TwittSerializer.deserialize(updated_twit)

        if not isinstance(updated_twit, Twitt):
            print("Передан некорректный формат для обновления твита.")
            return

        if twit_number < 0 or twit_number >= len(self.__twits):
            print("Некорректный номер твита.")
            return

        self.__twits[twit_number] = TwittSerializer.serialize(updated_twit)


class Twitt:
    """
    Класс самого твита
    """
    def __init__(self, title, text, time, comments=None, ratings=None):
        """
        Фукция инициализации самого твита
        :param title:
        :param text:
        :param time:
        :param comments:
        :param ratings:
        """
        self.title = title
        self.text = text
        self.ratings = ratings if ratings is not None else []
        self.comments = comments if comments is not None else []
        self.time = time

    def add_comment(self, comment):
        """
        метод для добавления комментария в твит
        :param comment: текст комментария
        :return: ничего не возвращает
        """
        self.comments.append(comment)

    def display_tweet(self):
        """
        Метод для отображения информации о твите.
        """
        print(f"Заголовок: {self.title}")
        print(f"Текст: {self.text}")
        print(f"Время: {self.time}")
        print("---")

    def tweet_info(self):
            print(f"Заголовок: {self.title}\n"
            f"Дата: {self.time}\n"
            f"Текст: {self.text}\n"
            f"Рейтинг: {self.ratings}\n"
            f"Комментарии: {self.comments}")

    def update_tweet(self, user, twit_number):
        """
        Метод для обновления твита пользователя.
        :param user: объект пользователя
        :param twit_number: номер твита
        :return: ничего не возвращает
        """

        if not user.is_valid_tweet_number(twit_number):
            print("Некорректный номер твита.")
            return

        new_title = input("Введите новый заголовок твита: ")
        new_text = input("Введите новый текст твита: ")

        # Обновляем данные твита
        self.title = new_title
        self.text = new_text

        user.update_tweet_in_list(self, twit_number)

        print("Твит успешно обновлен.")

    # def get_avg_score(self, twit_number):
    #     """
    #     Метод для получения средней оценки твита.
    #     :param twit_number: номер твита
    #     :return: средняя оценка твита
    #     """
    #     twit_dict = self.__twits[twit_number]
    #     twit = TwittSerializer.deserialize(twit_dict)
    #     ratings = twit.ratings
    #
    #     if not ratings:
    #         print("Твит не имеет оценок.")
    #         return
    #
    #     avg_score = round(sum(ratings) / len(ratings), 2)
    #     print(f"Средняя оценка твита: {avg_score}")
    #     return avg_score

    def get_avg_score(self):
        """
        Метод для получения средней оценки твита.
        :return: средняя оценка твита
        """
        if not self.ratings:
            print("Твит не имеет оценок.")
            return

        avg_score = round(sum(self.ratings) / len(self.ratings), 2)
        print(f"Средняя оценка твита: {avg_score}")
        return avg_score


class TwittSerializer:
    """
    класс для серилиазации / десеарилизации объетов твитов
    """
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
            time=datetime.fromisoformat(twit_dict["time"]),
            comments=twit_dict["comments"],
            ratings=twit_dict["ratings"]
        )


class UserSerializer:
    """
    класс для серилиазации / десеарилизации объетов пользователей
    """
    @staticmethod
    def serialize(user):
        """
        Метод преобразует объект пользователя в словарь.
        :param user: объект пользователя
        :return: словарь с данными пользователя
        """
        return {
            'login': user.login,
            'password': user.password,
            'twits': user.twits
        }

    @staticmethod
    def deserialize(user_dict):
        """
        Метод создает экземпляр класса User из словаря.
        :param user_dict: словарь с данными пользователя
        :return: экземпляр класса User
        """
        if user_dict is None:
            return
        login = user_dict.get('login')
        password = user_dict.get('password')
        twits = user_dict.get('twits')

        return User(login, password, twits)
