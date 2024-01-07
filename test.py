import requests
import json
import time


def get_employers(emploer):
    """Метод вывода вакансий на HH.RU"""

    # параметры, передаваемые в GET запросе
    params = {
        "per_page": 100,
        # "area": 113,                      # Регион работодателя
        # "text": f"NAME:{emploer}",        # Текст, встречающийся в имени работодателя
        # "only_with_vacancies": True,      # Только открытые вакансии
        "sort_by": "by_vacancies_open",     # Сортировка по количеству открытых вакансий по убыванию
    }

    # Список найденных работодателей
    employers = []

    # Выод общего количества найденных работодателей
    count_of_employers = requests.get('https://api.hh.ru/employers', params=params).json()["found"]
    print(f"Количество найденных работодателей на hh.ru = {count_of_employers}")

    # Вычисляем колличество страниц для отображения работодателей
    page_count = count_of_employers // 100
    if page_count >= 20:
        page_count = 20
    elif (count_of_employers % 100) > 0:
        page_count += 1
    print(f"Количество страниц = {page_count}")

    # Формирование списка работодателей
    for page in range(page_count):
        params["page"] = page
        data_list = requests.get('https://api.hh.ru/employers', params=params).json()["items"]
        employers.extend(data_list)
        time.sleep(0.2)

    # print(f"Количество работодателей с наибольшим числом открытых вакансий =\n{len(employers)}")

    # Выод в консоль полученного списка работодателей
    for employ in employers:
        print(f"ID компании: {employ['id']}; "
              f"Название компании: {employ['name']}; "
              f"Количество открытых вакансий: {employ['open_vacancies']} ")

    # req = requests.get('https://api.hh.ru/employers', params=params)
    # print(req.json()["items"])
    # print(req.json()["found"])
    # data = req.content.decode()
    # req.close()
    # count_of_employers = json.loads(data)['found']

    # data_list = json.loads(data)['items']
    # i = 0
    # j = count_of_employers
    # print(j)
    # print(len(data_list))
    # for dat in data_list:
    #     print(dat)
    # while i < j:
    #     req = requests.get(f'https://api.hh.ru/employers/{str(i + 1)}')
    #     data = req.content.decode()
    #     req.close()
    #     js_obj = json.loads(data)
    #     try:
    #         employers.append([js_obj['id'], js_obj['name']])
    #         i += 1
    #         print([js_obj['id'], js_obj['name']])
    #     except:
    #         i += 1
    #         j += 1
    #     if i % 200 == 0:
    #         time.sleep(0.2)
    # return employers


def get_vacancies(params: dict):

    req = requests.get('https://api.hh.ru/vacancies', params=params)
    data = req.content.decode()
    req.close()
    count_of_vacancy = json.loads(data)['found']
    vacancy_list = json.loads(data)['items']
    if count_of_vacancy == 0:
        return None
    # print(count_of_vacancy)
    # print(len(vacancy_list))
    # for dat in vacancy_list:
    #     print(dat)
    return count_of_vacancy, vacancy_list
