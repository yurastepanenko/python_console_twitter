from presenter import *
from models import *
from db_presenter import database_initialization, read_database, write_database

while True:
    # создаем базу данных если ее не было
    database_initialization()

    # для оптимизации нашего приложения считываем 1 раз файл, и потом с этим продолжаем работать
    db = read_database()

    show_menu(main_menu_list)
    choice = input("Выберите один из пунктов меню\n")

    if choice == '1':
        # обновляем базу в "оперативке"
        db = registration(db)

        # обновляем сам файл
        write_database(db)

    elif choice == '2':
        current_user = login(db)
        user_actions(db, current_user)

    elif choice == '0':
        print("Вы выбрали завершение работы! Удачного дня!")
        break

    else:
        print("Такого пункта меню не существует или он в разработке:) Попробуйте еще раз!")
