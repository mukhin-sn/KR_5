import json
import time

import requests


class HhClass:
    """
    Класс для работы с запросами к сайту hh.ru
    """

    def __init__(self, url: str, params: dict):
        self.url = url  # Адрес GET-запроса
        self.params = params  # Параметры GET-запроса
        self.data_list = []  # Список найденных записей

        # количество найденых записей
        self.count_of_data_list = (requests.get(self.url, params=self.params).json())["found"]

    def __str__(self):
        return f"{self.__class__.__name__}"

    def __repr__(self):
        return (f"host-url = {self.url}\n"
                f"PARAMS -> {[key_val for key_val in self.params.items()]}\n"
                f"Number of records found = {self.count_of_data_list}\n"
                f"стр. {self.page_count()}")

    def get_data(self) -> list:
        """
        Метод получения данных с сайта hh.ru
        :return: Список полученных, в результате GET-запроса, данных
        """

        for page in range(self.page_count()):
            self.params["page"] = page
            temp_data_list = requests.get(self.url, params=self.params).json()["items"]
            self.data_list.extend(temp_data_list)
            time.sleep(0.2)

        return self.data_list

    def print_data_list(self) -> list:
        """ Метод вывода в консоль полученного, в результате GET-запроса, списка """

        if not self.data_list:
            self.get_data()
            print(f"Всего записей: {len(self.data_list)}")

        temp_data_list = []
        for dl in self.data_list:
            print(dl)
            temp_dic = dict(
                id_empl=dl['employer']['id'],
                name_empl=dl['employer']['name'],
                id_vac=dl['id'],
                name_vac=dl['name'],
            )
            temp_data_list.append(temp_dic)
            # print(f"ID employer: {dl['employer']['id']}; "
            #       f"Название компании: {dl['employer']['name']}; "
            #       f"ID вакансии: {dl['id']}; "
            #       f"Название вакансии: {dl['name']}"
            #       # f"Количество открытых вакансий: {dl['open_vacancies']}"
            #       )
        return temp_data_list

    def page_count(self) -> int:
        """
        Метод вычисляет колличество страниц для отображения записей
        :return: число страниц
        """

        page_count = self.count_of_data_list // 100
        if page_count >= 20:
            page_count = 20
        elif (self.count_of_data_list % 100) > 0:
            page_count += 1
        return page_count

    def save_to_file(self, file_name: str, dt_lst: list) -> None:
        """
        Метод сохраняет полученные данные в файл
        :param file_name: имя файла
        :param dt_lst: список сохраняемых данных
        :return:
        """
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(dict(object=dt_lst), file)

    def load_from_file(self, file_name) -> list:
        """
        Метод загрузки данных из *.json файла в список
        :param file_name: имя файла
        :return: список словарей из *.json файла
        """
        with open(file_name, "r") as file:
            out_list = json.load(file)
            return out_list


###############################################################################################################

# url = "https://api.hh.ru/employers"
# params = {
#         "per_page": 100,
#         "area": 1,                      # Регион работодателя
#         # "text": f"NAME:{data}",           # Текст, встречающийся в имени работодателя
#         # "only_with_vacancies": True,      # Только открытые вакансии
#         "sort_by": "by_vacancies_open",     # Сортировка по количеству открытых вакансий по убыванию
#     }
#
# employ_class = HhClass(url, params)
# print(employ_class)
# print(repr(employ_class))
# employ_class.print_data_list()
#
# print("=" * 300 + "\n")

url = "https://api.hh.ru/vacancies"
# text = 'Python'
emp_id = 5178281
params = {
    "per_page": 100,
    "area": 113,
    # "text": f"NAME:{text}",
    "employer_id": emp_id,
    "only_with_salary": True,
}

vac_class = HhClass(url, params)
print(vac_class)
print(repr(vac_class))
# data_lst = vac_class.print_data_list()

# vac_class.save_to_file('vacancy_data.json', data_lst)

# file_data = vac_class.load_from_file("vacancy_data.json")
# for i in file_data['object']:
#     print(i['id_empl'])

