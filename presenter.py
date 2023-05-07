from models import user_menu_actions


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
    else:
        print(f"Пользователь {login} уже существует! повторите попытку!")

    return db


def login(db):
    """
    функция которая позволяет пользователю залогиниться
    :param db: наша база данных
    :return: возвращает нашего пользователя(объект)
    """
    login = input("Введите ваш логин: ")
    password = input("Введите ваш пароль: ")
    for user_data in db:
        if user_data["login"] == login:
            user = User(user_data["login"], user_data["password"])
            if user.check_data(login, password):
                print("Вы успешно авторизовались:)")
                return user
        else:
            print("Некорректный логин или пароль:(")
            return None

@data_exists
def user_actions(db, current_user):
    while True:
        show_menu(user_menu_actions)
        choice = input("Выберите один из пунктов меню\n")
        if choice == '1':
            show_all_tweets(current_user)

        elif choice == '2':
            work_with_single_twit(db, current_user)

        elif choice == '3':
            view_other_accounts(db, current_user)

        elif choice == '0':
            break

        else:
            print("Такого пункта меню не существует или он в разработке:) Попробуйте еще раз!")


def show_all_tweets(current_user):
    """
    функция, которая вернет все заметки текущего пользователя
    :param current_user: текущий пользователь
    :return: ничего не возвращает
    """
    current_user.view_all_notes()


def work_with_single_twit(db, current_user):
    print("work_with_single_twit")


def view_other_accounts(db, current_user):
    print("view_other_accounts")


class User:
    def __init__(self, login, password):
        self.__login = login
        self.__password = password
        self.__notes = []

    @property
    def login(self):
        return self.__login

    @property
    def notes(self):
        return self.__notes

    def check_data(self, login, password):
        if self.__login == login and self.__password == password:
            return True
        else:
            return False

    def __str__(self):
        return self.__login

    def to_dict(self):
        """
        метод привод объект юзера к словарю
        :return: возвращает словарь(сконвертированного юзера)
        """
        return {
            'login': self.__login,
            'password': self.__password,
            'notes': self.__notes
        }

    def view_all_notes(self):
        """
        Метод для просмотра всех заметок пользователя.
        """
        if self.__notes:
            print("Список заметок:")
            for note in self.__notes:
                print(f"Заголовок: {note.title}")
                print(f"Текст: {note.text}")
                print("---")
        else:
            print("У вас пока нет заметок.")


class Notes:
    def __init__(self):
        self.title = input("title")
        self.text = input("text")
        self.ratings = []
        self.comments = []
