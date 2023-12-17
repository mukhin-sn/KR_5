import requests
import json
import time


def get_employers():
    """Метод вывода всех вакансий на HH.RU"""
    req = requests.get('https://api.hh.ru/employers')
    data = req.content.decode()
    req.close()
    count_of_employers = json.loads(data)['found']
    employers = []
    i = 0
    j = count_of_employers
    print(j)
    while i < j:
        req = requests.get('https://api.hh.ru/employers/' + str(i + 1))
        data = req.content.decode()
        req.close()
        js_obj = json.loads(data)
        try:
            employers.append([js_obj['id'], js_obj['name']])
            i += 1
            print([js_obj['id'], js_obj['name']])
        except:
            i += 1
            j += 1
        if i % 200 == 0:
            time.sleep(0.2)
    return employers


employers = get_employers()
