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

    def get_data(self, param=None) -> list:
        """
        Метод получения данных с сайта hh.ru
        :return: Список полученных, в результате GET-запроса, данных
        """

        if param is None:
            param = self.params
        for page in range(self.page_count()):
            param["page"] = page
            temp_data_list = requests.get(self.url, params=param).json()["items"]
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
            # print(dl)
            temp_dic = dict(
                id_empl=dl['employer']['id'],
                name_empl=dl['employer']['name'],
                id_vac=dl['id'],
                name_vac=dl['name'],
            )
            temp_data_list.append(temp_dic)
            print(f"ID employer: {dl['employer']['id']}; "
                  f"Название компании: {dl['employer']['name']}; "
                  f"ID вакансии: {dl['id']}; "
                  f"Название вакансии: {dl['name']}"
                  # f"Количество открытых вакансий: {dl['open_vacancies']}"
                  )
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

    @staticmethod
    def save_to_file(file_name: str, dt_lst: list) -> None:
        """
        Метод сохраняет полученные данные в файл
        :param file_name: имя файла
        :param dt_lst: список сохраняемых данных
        :return:
        """
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(dict(object=dt_lst), file)

    @staticmethod
    def load_from_file(file_name) -> list:
        """
        Метод загрузки данных из *.json файла в список
        :param file_name: имя файла
        :return: список словарей из *.json файла
        """
        with open(file_name, "r", encoding="utf-8") as file:
            out_list = json.load(file)
            return out_list

    def id_employers_filter(self):
        if not self.data_list:
            self.get_data()
        print(f"Всего записей: {len(self.data_list)}")
        out_list = []
        for val_dic in self.data_list:
            out_list.append(val_dic['employer']['id'])
        out_list = set(out_list)
        return list(out_list)

    @staticmethod
    def print_data(data_list: list[tuple]) -> None:
        """
        Метод вывода в консоль данных
        :param data_list: список выводимых в консоль данных
        :return:
        """
        for line in data_list:
            for s_data in range(len(line)):
                print(f'{line[s_data]}  ', end='')
            print()



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
text = 'Python'
# emp_id = 5178281
params = {
    "per_page": 100,
    "area": 113,
    "text": f"NAME:{text}",
    # "employer_id": emp_id,
    "only_with_salary": True,
}

# vac_class = HhClass(url, params)
# print(vac_class)
# print(repr(vac_class))
# data_lst = vac_class.print_data_list()
# out_lst = vac_class.get_data()

# filter_id = vac_class.id_employers_filter()
# print(len(filter_id))
# vac_class.save_to_file('filter_id.json', filter_id)

# vac_class.save_to_file('out_vac.json', out_lst)
# vac_class.save_to_file('vacancy_data.json', data_lst)

# file_data = HhClass.load_from_file("filter_id.json")
# print(len(file_data['object']))
# # for i in file_data['object']:
# #     print(i)
# temp_list = []
# for obj_files in file_data['object']:
#     params = {
#         "per_page": 100,
#         "area": 113,
#         # "text": f"NAME:{text}",
#         "employer_id": obj_files,
#         "only_with_salary": True,
#     }
#     vacancy_data = HhClass(url, params)
#     _data = vacancy_data.get_data()
#     out_data = {obj_files: _data}
#     temp_list.append(out_data)
#     print(f"id: {obj_files}; "
#           f"found: {vacancy_data.count_of_data_list} = {len(_data)}")
#
# HhClass.save_to_file('out_vac.json', temp_list)
