from src.db_data import *
from src.hh_class import *
from src.menu_handler import *


def main():
    db_name = "hh_ru"
    db_params = {
        "host": "localhost",
        "database": db_name,
        "user": "postgres",
        }

    url_employers = 'https://api.hh.ru/employers'
    url_vacancies = 'https://api.hh.ru/vacancies'

    params_employers = {
        'per_page': 100,
        'area': 113,                        # Регион работодателя
        # 'text': f'NAME:{data}',           # Текст, встречающийся в имени работодателя
        'only_with_vacancies': True,        # Только открытые вакансии
        'sort_by': 'by_vacancies_open',     # Сортировка по количеству открытых вакансий (по убыванию)
        }

    params_vacancies = {
        'per_page': 100,
        'area': 113,
        # 'text': f'NAME:{text}',
        # "employer_id": emp_id,
        'only_with_salary': True,
        }

    db_object = DBManager(**db_params)
    db_object.create_table(sql_for_employers_create)
    db_object.create_table(sql_for_vacancies_create)

    employers_object = EmployersHhClass(url_employers, '', **params_employers)
    vacancies_object = HhClass(url_vacancies, **params_vacancies)

    menu_handler = MenuHandler(db_object, vacancies_object, employers_object)
    menu_handler.menu_one_handler()

    # print(db_object.get_id_employers())
    # text = 'python, django'
    # temp_data = db_object.get_vacancies_with_higher_salary()
    #
    # db_object.print_data_db(temp_data)

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
    # emp_id = '49357'  # '1455'
    # area = 113
    # params = {
    #     "per_page": 100,
    #     "area": area,
    #     # "text": f"NAME:{txt}",
    #     "employer_id": emp_id,
    #     "only_with_salary": True,
    #     }
    #
    # for i in range(20):
    #     print("=" * 300)
    #     params["page"] = i
    #     vac = get_vacancies(params)
    #     # print(vac[0])
    #     for j in vac[1]:
    #         print(j)
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

    # # Берём данные из сохраненного файла
    # data_list = HhClass.load_from_file('src/out_vac.json')
    # data_list = data_list['object']
    #
    # # Определяем количество нужных записей
    # count = len(data_list)
    #
    # # Формируем словарь и список из ID - работодателей и количества открытых ими вакансий
    # out_list = []
    # out_dict = {}
    # for val_lst in data_list:
    #     for key, val in val_lst.items():
    #         out_dict.update({key: len(val)})
    #         out_list.append(dict(id=key, found_vacancy=len(val)))
    #
    # for i in out_list:
    #     print(i)

    # Сохраняем полученный список в файл, для дальнейшей обработки
    # HhClass.save_to_file('src/found_vacancy.json', out_list)

    # params_db = {
    #     "host": "localhost",
    #     "database": "north",
    #     "user": "postgres",
    # }
    # passwrd = input('Введите пароль для входа в базу данных -> ')
    # db_func = DBManager(**params_db)
    # lst_print = db_func.db_connect()
    # lst_print = db_func.get_companies_and_vacancies_count()
    # HhClass.print_data(lst_print)
