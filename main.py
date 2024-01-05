from src.hh_areas import *
from test import get_employers, get_vacancies


def main():
    db_name = "hh_ru"

    # Тестирование функции get_employers()
    # ===============================================
    # emplr = 'Газпром'
    # get_employers(emplr)

    # get_employers('')
    # print('-' * 300 + "\n")
    # ===============================================

    # Тестирование функции get_vacancies()
    # ===============================================
    # txt = "Python"
    # employers_id = '49357'  # '1455'
    # areas = 113
    # vacan = get_vacancies(txt, employers_id, areas)
    # print(vacan[0])
    # for i in vacan[1]:
    #     print(i)
    # ===============================================

    # Тестирование функции get_areas()
    # ===============================================
    areas = get_areas()
    # print(len(areas))
    # for ar in areas:
    #     print(ar, len(ar[3]))
    # ===============================================

    # Тестирование функции areas_load_to_db()
    # ===============================================
    password = input('Введите пароль от базы данных -> ')
    areas_load_to_db(db_name, password, areas)
    # ===============================================

    # Тестирование функции create_database()
    # ===============================================
    # password = input('Введите пароль от базы данных -> ')
    # create_database("db_hh", password)
    # ===============================================



if __name__ == '__main__':
    main()

