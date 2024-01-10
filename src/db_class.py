import psycopg2


class DBManager:
    """
    Класс для работы с данными в БД
    """

    def __init__(self, password, host="localhost", database="postgres", user="postgres"):
        self.host = host
        self.user = user
        self.database = database
        self.password = password

    def get_companies_and_vacancies_count(self) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        :return:
        """
        out_lst = []
        conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        with conn:
            with conn.cursor() as cur:
                request = """
                SELECT * FROM customers
                """
                cur.execute(request)
                out_lst = cur.fetchall()
        conn.close()
        return out_lst

    def get_all_vacancies(self) -> list[dict]:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        :return:
        """
        out_lst = []
        conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        with conn:
            with conn.cursor() as cur:
                request = """
                        Здесь текст SQL запроса
                        """
                cur.execute(request)
                out_lst = cur.fetchall()
        conn.close()
        return out_lst

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по вакансиям
        :return:
        """
        average_salary = None
        out_lst = []
        conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        with conn:
            with conn.cursor() as cur:
                request = """
                        Здесь текст SQL запроса
                        """
                cur.execute(request)
                out_lst = cur.fetchall()
        conn.close()
        return average_salary

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Получает список всех вакансий, у которых зарплата выше средней
        по всем вакансиям
        :return:
        """
        out_lst = []
        conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        with conn:
            with conn.cursor() as cur:
                request = """
                        Здесь текст SQL запроса
                        """
                cur.execute(request)
                out_lst = cur.fetchall()
        conn.close()
        return out_lst

    def get_vacancies_with_keyword(self, text) -> list:
        """
        Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова
        :param text: список переданных в метод слов
        :return:
        """
        out_lst = []
        conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        with conn:
            with conn.cursor() as cur:
                request = """
                        Здесь текст SQL запроса
                        """
                cur.execute(request)
                out_lst = cur.fetchall()
        conn.close()
        return out_lst
