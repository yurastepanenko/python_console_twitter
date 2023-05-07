from presenter import *
from models import *

while True:
    show_menu(main_menu_list)
    choice = input("Выберите один из пунктов меню\n")

    if choice == '1':
        print("Регистрация")

    elif choice == '2':
        print("Авторизация")

    elif choice == '0':
        print("Вы выбрали завершение работы! Удачного дня!")
        break

    else:
        print("Такого пункта меню не существует или оно в разработке:) Попробуйте еще раз!")
