import json
import time
import requests


class HhClass:
    """
    Класс для работы с запросами к сайту hh.ru
    """

    def __init__(self, url: str, **params):
        self.url = url  # Адрес GET-запроса
        self.params = params  # Параметры GET-запроса
        self.data_list = []  # Список найденных записей

        # количество найденных записей
        if self.params == {}:
            self.count_of_data_list = 0
        else:
            self.count_of_data_list = (requests.get(self.url, params=self.params).json())["found"]

    def __str__(self):
        return f"{self.__class__.__name__}"

    def __repr__(self):
        return (f'host-url = {self.url}\n'
                f'PARAMS -> {[key_val for key_val in self.params.items()]}\n'
                f'Number of records found = {self.count_of_data_list}\n'
                f'стр. {self.page_count()}')

    def page_count(self) -> int:
        """
        Метод вычисляет количество страниц для отображения записей
        :return: число страниц
        """

        page_count = self.count_of_data_list // 100
        if page_count >= 20:
            page_count = 20
        elif (self.count_of_data_list % 100) > 0:
            page_count += 1
        return page_count

    def get_data(self, param=None) -> list[tuple]:
        """
        Метод получения данных с сайта hh.ru
        :return: Список полученных, в результате GET-запроса, данных,
        готовых для передачи в базу данных
        """

        self.data_list = []
        if param is None:
            param = self.params
        for page in range(self.page_count()):
            param['page'] = page
            temp_data_list = requests.get(self.url, params=param).json()["items"]
            for tmp_lst in temp_data_list:
                temp_data_tuple = (tmp_lst['id'],
                                   tmp_lst['employer']['id'],
                                   tmp_lst['name'],
                                   tmp_lst['url'],
                                   tmp_lst['salary']['from'],
                                   tmp_lst['salary']['to'],
                                   tmp_lst['salary']['currency'],)
                self.data_list.append(temp_data_tuple)
            # self.data_list.extend(temp_data_list)
            time.sleep(0.2)

        return self.data_list

    # def data_list_to_db(self) -> list[tuple]:
    #     """
    #     Метод формирует список данных для передачи в базу  данных
    #     :return:
    #     """
    #     out_lst_tuple = []
    #     temp_tuple = ()
    #     for data in self.data_list:
    #         out_lst_tuple.append(temp_tuple)
    #     return out_lst_tuple

    def print_data_list(self):
        """ Метод вывода в консоль полученного, в результате GET-запроса, списка """

        if not self.data_list:
            self.get_data()
        print('ID вакансии | '
              'ID работодателя | '
              'Название вакансии | '
              'Ссылка на вакансию | '
              'Зарплата от | '
              'Зарплата до | '
              'Валюта')
        print('-' * 108)
        for dl in self.data_list:
            for tpl in dl:
                print(tpl, end=' | ')
            print()
        print(f'Всего записей: {len(self.data_list)}')

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

    def id_employers_filter(self) -> list:
        """
        Метод убирает повторяющиеся ID-работодателей
        :return:
        """
        if not self.data_list:
            self.get_data()
        out_list = []
        for val_dic in self.data_list:
            out_list.append(val_dic[1])
        out_list = set(out_list)
        print(f'Всего уникальных записей: {len(out_list)}')
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

    @staticmethod
    def get_text(txt: str) -> str:
        """
        Метод формирует строку для поля param['text']
        :param txt: Входная строка из которой формируется выходная строка
        :return: Выходная строка
        """
        # Формируем список из строки :param txt: удаляя запятые и пробелы
        word_list = [word.strip().lower() for word in txt.split(',')]

        # Формируем выходную строку
        return 'AND'.join(word_list)

    @staticmethod
    def get_list_id(request: str) -> list:
        """
        Метод возвращает список ID - работодателей
        :param request: строка, из которой надо выбрать ID
        :return: список ID работодателей
        """
        out_list = []
        temp_list = [word.strip().lower() for word in request.split(',')]
        for word in temp_list:
            if word.isdigit():
                out_list.append(word)
        out_list = set(out_list)
        return list(out_list)

    # @staticmethod
    # def employers_with_vacancies(employers_id) -> dict:
    #     """
    #     Метод ищет количество открытых вакансий у работодателя
    #     :return: словарь {employers_id: open_vacancies}
    #     """
    #     url = f"https://api.hh.ru/employers/{employers_id}"
    #     temp_data = requests.get(url).json()
    #     print(f'ID: {temp_data["id"]} | Название компании: {temp_data["name"]} | '
    #           f'количество открытых вакансий: {temp_data["open_vacancies"]}')
    #     return temp_data


class EmployersHhClass(HhClass):

    def __init__(self, url: str, employer_id: str, **params):
        super().__init__(url, **params)
        self.employer_id = employer_id
        self.url = url

        # количество открытых вакансий
        if self.employer_id == '':
            self.count_of_data_list = 0
        else:
            self.count_of_data_list = (requests.get(f'{self.url}/{self.employer_id}').json())["open_vacancies"]

        # self.count_of_data_list = (requests.get(self.url).json())["open_vacancies"]

    def get_data(self, **kwargs) -> list[tuple]:
        """
        Метод возвращает список данных по работодателю
        :param kwargs:
        :return:
        """
        self.data_list = []
        # print(f'{self.url}/{self.employer_id}')
        temp_dict = requests.get(f'{self.url}/{self.employer_id}').json()
        try:
            self.data_list.append((temp_dict['id'],
                                   temp_dict['name'],
                                   temp_dict['open_vacancies'],
                                   temp_dict['site_url']))
        except KeyError:
            print(f'Работодатель с ID {self.employer_id} не найден')
            return None

        return self.data_list

    def print_data_list(self):
        """ Метод вывода в консоль полученного, в результате GET-запроса, списка """

        if not self.data_list:
            self.get_data()
        print('ID работодателя | '
              'Название работодателя | '
              'Количество открытых вакансий | '
              'Ссылка на работодателя')
        print('-' * 96)
        for dl in self.data_list:
            for tpl in dl:
                print(tpl, end=' | ')
            print()

###############################################################################################################

# employer_id = "41862"
# url = f"https://api.hh.ru/employers/{employer_id}"
# temp_data = requests.get(url).json()
# print(f'{temp_data["id"]} | {temp_data["name"]} | {temp_data["open_vacancies"]} | {temp_data["site_url"]}')

# for i in temp_data:
# print(i, end=': ')
# print(temp_data[i])
# print(temp_data)

# url = "https://api.hh.ru/employers"
# data = ''

# params = {
#         "per_page": 100,
#         "area": 113,                      # Регион работодателя
#         # "text": f"NAME:{data}",           # Текст, встречающийся в имени работодателя
#         "only_with_vacancies": True,      # Только открытые вакансии
#         "sort_by": "by_vacancies_open",     # Сортировка по количеству открытых вакансий по убыванию
#     }
# employer_id = '41862'
# params['text'] = f'!COMPANY_ID:{employer_id}'

# empl_obj = EmployersHhClass(url, employer_id)
# print(repr(empl_obj))
# print(empl_obj.get_data())
# empl_obj.print_data_list()

# employ_class = HhClass(url, **params)
# print(employ_class)
# print(repr(employ_class))
# employ_class.print_data_list()
#
# print("=" * 300 + "\n")

# url = 'https://api.hh.ru/vacancies'
# text = 'Python'
# emp_id = 5178281
# params = {
#     'per_page': 100,
#     'area': 113,
#     # 'text': f'NAME:{text}',
#     "employer_id": emp_id,
#     'only_with_salary': True,
# }

# vac_class = HhClass(url, **params)
# # print(vac_class)
# # print(repr(vac_class))
# data_lst = vac_class.print_data_list()
# out_lst = vac_class.get_data()
# print(out_lst)
# for i in out_lst:
#     print(i)


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
#     vacancy_data = HhClass(url, **params)
#     _data = vacancy_data.get_data()
#     out_data = {obj_files: _data}
#     temp_list.append(out_data)
#     print(f"id: {obj_files}; "
#           f"found: {vacancy_data.count_of_data_list} = {len(_data)}")
#
# HhClass.save_to_file('out_vac.json', temp_list)
