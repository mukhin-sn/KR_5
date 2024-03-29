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

    def count_of_data_list(self, **params):
        """
        Метод возвращает количество найденных записей
        :param params: параметры запроса
        :return:
        """
        if params == {}:
            count_of_data_list = 0
        else:
            count_of_data_list = (requests.get(self.url, params=params).json())["found"]
        return count_of_data_list

    def __str__(self):
        return f"{self.__class__.__name__}"

    def __repr__(self):
        return (f'host-url = {self.url}\n'
                f'PARAMS -> {[key_val for key_val in self.params.items()]}\n'
                f'Number of records found = {self.count_of_data_list(**self.params)}\n'
                f'стр. {self.page_count()}')

    def page_count(self, **params) -> int:
        """
        Метод вычисляет количество страниц для отображения записей
        :return: число страниц
        """

        page_count = self.count_of_data_list(**params) // 100
        if page_count >= 20:
            page_count = 20
        elif (self.count_of_data_list(**params) % 100) > 0:
            page_count += 1
        return page_count

    def get_data(self, **param) -> list[tuple]:
        """
        Метод получения данных с сайта hh.ru
        :return: Список полученных, в результате GET-запроса, данных,
        готовых для передачи в базу данных
        """

        param['per_page'] = 100
        param['area'] = 113
        param['only_with_salary'] = True

        data_list = []
        if param is None:
            param = self.params
        for page in range(self.page_count(**param)):
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
                data_list.append(temp_data_tuple)
            time.sleep(0.2)
            self.data_list = data_list
        return data_list

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
        return ' AND '.join(word_list)

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


class EmployersHhClass(HhClass):

    def __init__(self, url: str, employer_id: str, **params):
        super().__init__(url, **params)
        self.employer_id = employer_id
        self.url = url

    def count_of_data_list(self, **params):
        """
        Метод возвращает количество найденных записей
        :param params: параметры запроса
        :return:
        """
        if params == {}:
            count_of_data_list = 0
        else:
            count_of_data_list = (requests.get(self.url, params=params).json())["open_vacancies"]
        return count_of_data_list

    def get_data(self, **kwargs) -> list[tuple]:
        """
        Метод возвращает список данных по работодателю
        :param kwargs:
        :return:
        """
        data_list = []
        temp_dict = requests.get(f'{self.url}/{self.employer_id}').json()
        try:
            data_list.append((temp_dict['id'],
                              temp_dict['name'],
                              temp_dict['open_vacancies'],
                              temp_dict['site_url']))
        except KeyError:
            return None
        self.data_list = data_list
        return data_list

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

    @staticmethod
    def id_employers_filter(vac_list: list[tuple]) -> list:
        """
        Метод убирает повторяющиеся ID-работодателей
        :return:
        """
        if not vac_list:
            return []
        out_list = []
        for vac in vac_list:
            out_list.append(vac[1])
        out_list = set(out_list)
        print(f'Всего уникальных записей: {len(out_list)}')
        return list(out_list)
