import psycopg2
import requests
import json
from test import *


def get_areas() -> list:
    """
    Метод формирования списка регионов сайта hh.ru
    :return: список кортежей с id и именами регионов (городов)
    """
    req = requests.get('https://api.hh.ru/areas')
    data = req.content.decode()
    req.close()
    js_obj = json.loads(data)
    areas = []
    for k in js_obj:
        for i in range(len(k['areas'])):
            if len(k['areas'][i]['areas']) != 0:  # Если у зоны есть внутренние зоны
                for j in range(len(k['areas'][i]['areas'])):
                    areas.append((k['id'],
                                  k['name'],
                                  k['areas'][i]['areas'][j]['id'],
                                  k['areas'][i]['areas'][j]['name']))
            else:  # Если у зоны нет внутренних зон
                areas.append((k['id'],
                              k['name'],
                              k['areas'][i]['id'],
                              k['areas'][i]['name']))
    return areas


# params_db = {
#     "host": "localhost",
#     "database": "hh",
#     "user": "postgres",
#     # "password": "835221",
# }


# def fun_a(**pdb):
#     # try:
#     #     host = pdb['host']
#     #     db = pdb['database']
#     #     usr = pdb['user']
#     # except KeyError:
#     #     return None
#     for i in pdb:
#         print(pdb[i])
#
#     try:
#         print(pdb['password'])
#     except KeyError:
#         pdb['password'] = input("Введите пароль базы данных -> ")
#
#     print(pdb['password'])
#     return pdb
#
#
# b = fun_a(**params_db)
# print(b)


def create_database(db_name: str, password: str) -> None:
    """
    Метод создания базы данных
    :param db_name: имя базы данных
    :param password: пароль для подключения к базе данных
    :return: None
    """
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password=password
    )
    conn.autocommit = True
    try:
        cur = conn.cursor()
        cur.execute(f'CREATE DATABASE {db_name}')
    except psycopg2.errors.DuplicateDatabase:
        print('Уже есть база')
    finally:
        cur.close()
        conn.close()


def areas_load_to_db(db_name: str, password: str, data_list: list) -> None:
    """
    Метод формирования таблицы базы данных с регионами и городами
    :param db_name: имя базы данных
    :param password: пароль для подключения к базе данных
    :param data_list: список кортежей для записи в базу данных
    :return: None
    """
    conn = psycopg2.connect(
        host='localhost',
        database=db_name,
        user='postgres',
        password=password
    )
    try:
        with conn:
            with conn.cursor() as cur:
                try:
                    out_data = """
                    CREATE TABLE areas
                    (
                    areas_id int,
                    areas_name varchar(30) NOT NULL,
                    area_id int PRIMARY KEY,
                    area_name varchar(80) NOT NULL
                    )
                    """
                    cur.execute(out_data)
                except psycopg2.errors.DuplicateTable:
                    pass
                    # print("Запись существует")
                for dl_var in data_list:
                    try:
                        cur.executemany(f'INSERT INTO areas VALUES (%s, %s, %s, %s)', dl_var)
                    except psycopg2.errors.InFailedSqlTransaction:
                        pass
                        # print('Дубль')
    finally:
        conn.close()

#########################################################################################


# areas = get_areas()
# print(len(areas))
# rus_ars = []
# for ars in areas:
#     if int(ars[0]) == 113:
#         rus_ars.append([ars[2], ars[3]])
#     # print(ars)
# print(len(rus_ars))
# try:
#     for r_ars in rus_ars:
#         vacancy_id = get_vacancies("Python", '9245413', int(r_ars[0]))
#         if vacancy_id is not None:
#             print(r_ars)
#             for vac in vacancy_id[1]:
#                 print(vac)
#             print(vacancy_id[0])
#             print("-" * 50)
#         else:
#             continue
# except KeyboardInterrupt:
#     print('Пользователь прервал программу')
