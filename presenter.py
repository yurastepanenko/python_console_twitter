def show_menu(menu_list):
    """
    ф-ия , которая отображает основное меню
    @menu_list - словарь, который будем отображать
    """
    for key, value in menu_list.items():
        print(key, value)