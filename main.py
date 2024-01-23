from src.db_data import *
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


if __name__ == '__main__':
    main()
