import requests
import json
from test import *


def get_areas():
    req = requests.get('https://api.hh.ru/areas')
    data = req.content.decode()
    req.close()
    js_obj = json.loads(data)
    areas = []
    for k in js_obj:
        for i in range(len(k['areas'])):
            if len(k['areas'][i]['areas']) != 0:                      # Если у зоны есть внутренние зоны
                for j in range(len(k['areas'][i]['areas'])):
                    areas.append([k['id'],
                                  k['name'],
                                  k['areas'][i]['areas'][j]['id'],
                                  k['areas'][i]['areas'][j]['name']])
            else:                                                                # Если у зоны нет внутренних зон
                areas.append([k['id'],
                              k['name'],
                              k['areas'][i]['id'],
                              k['areas'][i]['name']])
    return areas

#########################################################################################


areas = get_areas()
print(len(areas))
rus_ars = []
for ars in areas:
    if int(ars[0]) == 113:
        rus_ars.append([ars[2], ars[3]])
    # print(ars)
print(len(rus_ars))
try:
    for r_ars in rus_ars:
        vacancy_id = get_vacancies("Python", '9245413', int(r_ars[0]))
        if vacancy_id is not None:
            print(r_ars)
            for vac in vacancy_id[1]:
                print(vac)
            print(vacancy_id[0])
            print("-" * 50)
        else:
            continue
except KeyboardInterrupt:
    print('Пользователь прервал программу')





