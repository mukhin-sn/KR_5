import psycopg2


class DBManager:
    """
    Класс для работы с данными в БД
    """

    def __init__(self, **params):
        self.params = params
        self.conn = None
        self.cur = None
        self.sql_request = ''
        try:
            psw = self.params['password']
        except KeyError:
            self.params['password'] = input('Введите пароль для соединения с базой данных -> ')

        self.db_create()

    def db_connect(self, auto_comm=False, **params):
        """
        Метод устанавливает соединение с базой данных
        """
        while True:  # цикл повторяется, пока не введен верный пароль
            try:
                self.conn = psycopg2.connect(**params)
            except: #psycopg2.OperationalError: # UnicodeDecodeError:
                print('PASSWORD - ERROR\nПопробуйте ещё раз')
            else:
                break
            params['password'] = input('-> ')
        self.params['password'] = params['password']
        self.conn.autocommit = auto_comm
        self.cur = self.conn.cursor()

    def db_disconnect(self):
        """
        Метод закрывает соединение с базой данных
        """
        self.cur.close()
        self.conn.commit()
        self.conn.close()

    def db_create(self):
        """
        Метод создания базы данных
        """
        params = self.params
        db_name = params['database']
        params['database'] = 'postgres'
        self.db_connect(auto_comm=True, **params)
        try:
            self.cur.execute(f'CREATE DATABASE {db_name}')
        except psycopg2.errors.DuplicateDatabase:
            # print('База данных существует')
            pass
        finally:
            params['database'] = db_name
            self.cur.close()
            self.conn.close()

    def create_table(self, package: str):
        """
        Метод создания таблицы
        :param package: данные для создания таблицы
        :return:
        """
        self.db_connect(**self.params)
        try:
            out_data = package
            self.cur.execute(out_data)
        except psycopg2.errors.DuplicateTable:
            pass
        finally:
            self.db_disconnect()

    def load_to_db(self, tab_name: str, data_list: list[tuple]):
        """
        Метод записи / добавления данных в базу данных
        :return:
        """
        self.db_connect(**self.params)

        try:
            # self.cur.execute(self.sql_request)
            out_str = f'INSERT INTO {tab_name} VALUES ({"%s, " * (len(data_list[0]) - 1)}%s)'
            self.cur.executemany(out_str, data_list)
        # Запись данных в базу
        # Проверка на повторение записи
        except psycopg2.errors.InFailedSqlTransaction:
            pass
        except psycopg2.errors.UniqueViolation:
            pass
        finally:
            self.db_disconnect()

    def get_id_employers(self) -> list:
        """
        Метод получения списка ID - работодателей из базы данных
        :return:
        """
        out_lst = []
        self.db_connect(**self.params)
        request = """
        SELECT employer_id FROM employers
        """
        self.cur.execute(request)
        list_tuple = self.cur.fetchall()
        self.db_disconnect()
        for id_ in list_tuple:
            out_lst.append(id_[0])
        return out_lst

    @staticmethod
    def print_data_db(data_list: list[tuple]):
        for tpl in data_list:
            for dt in tpl:
                print(dt, end=' | ')

    def get_companies_and_vacancies_count(self) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        :return:
        """
        self.db_connect(**self.params)
        request = """
        SELECT
        """
        self.cur.execute(request)
        out_lst = self.cur.fetchall()
        self.db_disconnect()
        return out_lst

    def get_all_vacancies(self) -> list[dict]:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        :return:
        """
        self.db_connect(**self.params)
        request = """
        SELECT
        """
        self.cur.execute(request)
        out_lst = self.cur.fetchall()
        self.db_disconnect()
        return out_lst

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по вакансиям
        :return:
        """
        average_salary = None
        self.db_connect(**self.params)
        request = """
        SELECT
        """
        self.cur.execute(request)
        out_lst = self.cur.fetchall()
        self.db_disconnect()
        return average_salary

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Получает список всех вакансий, у которых зарплата выше средней
        по всем вакансиям
        :return:
        """
        self.db_connect(**self.params)
        request = """
        SELECT
        """
        self.cur.execute(request)
        out_lst = self.cur.fetchall()
        self.db_disconnect()
        return out_lst

    def get_vacancies_with_keyword(self, text: str) -> list:
        """
        Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова
        :param text: строка, состоящая из переданных в метод слов
        :return:
        """

        # Формируем список из строки :param text:
        word_list = [word.strip().lower() for word in text.split(',')]

        self.db_connect(**self.params)
        request = """
        SELECT
        """
        self.cur.execute(request)
        out_lst = self.cur.fetchall()
        self.db_disconnect()
        return out_lst
