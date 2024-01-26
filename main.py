from src.db_data import *
from src.menu_handler import *
from src.config import config


def main():

    db_params = config(filename='src/database.ini')
    params_employers = config(filename='src/database.ini', section='employers')
    params_vacancies = config(filename='src/database.ini', section='vacancies')

    url_employers = 'https://api.hh.ru/employers'
    url_vacancies = 'https://api.hh.ru/vacancies'

    db_object = DBManager(**db_params)
    db_object.create_table(sql_for_employers_create)
    db_object.create_table(sql_for_vacancies_create)

    employers_object = EmployersHhClass(url_employers, '', **params_employers)
    vacancies_object = HhClass(url_vacancies, **params_vacancies)

    menu_handler = MenuHandler(db_object, vacancies_object, employers_object)
    menu_handler.menu_one_handler()


if __name__ == '__main__':
    main()
