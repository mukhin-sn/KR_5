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
    txt = "Python"
    emp_id = '49357'  # '1455'
    area = 113
    params = {
        "per_page": 100,
        "area": area,
        # "text": f"NAME:{txt}",
        "employer_id": emp_id,
        "only_with_salary": True,
        }

    for i in range(20):
        print("=" * 300)
        params["page"] = i
        vac = get_vacancies(params)
        # print(vac[0])
        for j in vac[1]:
            print(j)
    # ===============================================

    # Тестирование функции get_areas()
    # ===============================================
    # areas = get_areas()
    # print(len(areas))
    # for ar in areas:
    #     print(ar, len(ar[3]))
    # ===============================================

    # Тестирование функции areas_load_to_db()
    # ===============================================
    # password = input('Введите пароль от базы данных -> ')
    # areas_load_to_db(db_name, password, areas)
    # ===============================================

    # Тестирование функции create_database()
    # ===============================================
    # password = input('Введите пароль от базы данных -> ')
    # create_database("db_hh", password)
    # ===============================================



if __name__ == '__main__':
    main()

