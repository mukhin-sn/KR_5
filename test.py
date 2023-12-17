import requests
import json
import time


def get_employers(emploer):
    """Метод вывода всех вакансий на HH.RU"""

    # параметры, передаваемые в GET запросе
    params = {
        "per_page": 100,
        # "area": 113,
        # "text": f"NAME:{emploer}",
        "only_with_vacancies": True,
        "sort_by": "by_vacancies_open",
    }

    req = requests.get('https://api.hh.ru/employers', params=params)
    data = req.content.decode()
    req.close()
    count_of_employers = json.loads(data)['found']
    employers = []
    data_list = json.loads(data)['items']
    i = 0
    j = count_of_employers
    print(j)
    print(len(data_list))
    for dat in data_list:
        print(dat)
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


emplr = 'Газпром'
get_employers(emplr)
