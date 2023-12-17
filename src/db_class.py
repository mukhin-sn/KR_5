import psycopg2


class DBManager:
    """
    Класс для работы с данными в БД
    """
    def __init__(self):
        pass

    def get_companies_and_vacancies_count(self) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        :return:
        """
        pass

    def get_all_vacancies(self) -> list[dict]:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        :return:
        """
        pass

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по вакансиям
        :return:
        """
        pass

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Получает список всех вакансий, у которых зарплата выше средней
        по всем вакансиям
        :return:
        """
        pass

    def get_vacancies_with_keyword(self) -> list:
        """
        Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова
        :return:
        """
        pass

