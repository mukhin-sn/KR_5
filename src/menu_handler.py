from src.db_class import DBManager
from src.hh_class import HhClass


class MenuHandler:
    """
    Класс для работы с меню программы
    """

    def __init__(self, db_obj: DBManager):

        # Главное меню программы
        self.menu_1 = {'1': 'Работа с запросами к сайту hh.ru',
                       '2': 'Работа с базой данных',
                       '3': 'Выход из программы',
                       }

        # Меню работы с запросами к сайту hh.ru
        self.menu_2 = {'1': 'Поиск работодателей по ключевым словам',
                       '2': 'Поиск работодателей по ID',
                       '3': 'Сохранение результатов поиска',
                       '4': 'Выход в главное меню',
                       }

        # Меню работы с базой данных
        self.menu_3 = {'1': 'Получение списка всех компаний и количества вакансий у каждой компании',
                       '2': 'Получение списка всех вакансий с указанием названия компании, '
                            'названия вакансии, зарплаты и ссылки на вакансию',
                       '3': 'Получение средней зарплаты по вакансиям',
                       '4': 'Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям',
                       '5': 'Получение списка всех вакансий, в названии которых содержатся ключевые слова',
                       '6': 'Выход в главное меню',
                       }

        self.answers_list = {'1': 'да', '2': 'нет'}
        self.answer = ''
        self.hh_obj = ''
        self.db_obj = db_obj

    def __str__(self):
        return f'{self.__class__.__name__}'

    def __repr__(self):
        pass

    @staticmethod
    def out_message(text: str):
        """
        Метод вывода сообщения
        :param text: содержит текст сообщения
        :return: None
        """
        print(f"\n{text}\n{'-' * 50}")

    @staticmethod
    def input_answer():
        """
        Метод ввода ответа на запрос
        :return:
        """
        answer = input("-> ")
        return answer

    @staticmethod
    def check_answer(answer: str, answer_options: dict) -> bool:
        """
        Метод проверки ответа пользователя
        :param answer: - ответ пользователя
        :param answer_options: - допустимые варианты ответов
        :return: - True, если 'answer' есть в 'answer_options'
        """
        if answer in answer_options:
            return True
        return False

    def out_question(self, question: str, answers: dict):
        """
        Метод вывода вопроса пользователю
        :param question: - вопрос пользователю
        :param answers: - словарь с вариантами ответов
        """
        print(f"\n{question}\n{'-' * 50}")
        for key in answers:
            print(f"{key} - {answers[key]}")
        self.out_message("Введите номер выбранного варианта")

    def question_handler(self, answer_options: dict) -> str:
        """
        Метод обработки ответа на вопрос
        зацикливается, пока не будет введен существующий вариант,
        соответствущий ключу словаря с вариантами ответов.

        :param answer_options: - словарь с вариантами ответов
        :return: - ключ словаря, соответствующий ответу пользователя
        """
        answer = ""
        while not self.check_answer(answer, answer_options):
            answer = self.input_answer()
            if self.check_answer(answer, answer_options):
                return answer
            print("Такого варианта нет. Введите существующий вариант")
            continue

    def print_menu(self, menu: dict) -> str:
        """
        Метод выводит меню и возвращает выбранный вариант
        :param menu: выводимое в консоль меню
        :return: выбранный вариант
        """
        self.out_question('Сделайте выбор', menu)
        answer = self.question_handler(menu)
        return answer

    def menu_three_handler(self):
        """
        Метод обработки меню работы с базой данных
        """
        while True:
            self.answer = self.print_menu(self.menu_3)
            if self.answer == '6':
                break
            elif self.answer == '1':
                self.db_obj.get_companies_and_vacancies_count()
            elif self.answer == '2':
                self.db_obj.get_all_vacancies()
            elif self.answer == '3':
                self.db_obj.get_avg_salary()
            elif self.answer == '4':
                self.db_obj.get_vacancies_with_higher_salary()
            else:
                self.out_message('Введите поисковый запрос:\n'
                                 'Слова, которые должны быть в названии вакансии, '
                                 'перечислите через запятую')
                answer = self.input_answer()
                self.db_obj.get_vacancies_with_keyword(answer)

    def menu_two_handler(self):
        """
        Метод обработки меню работы с запросами к сайту hh.ru
        """
        while True:
            self.answer = self.print_menu(self.menu_2)
            if self.answer == '4':
                break
            elif self.answer == '1':
                pass
            elif self.answer == '2':
                pass
            else:
                pass

    def menu_one_handler(self):
        """
        Метод обработки главного меню программы
        """
        while True:
            self.answer = self.print_menu(self.menu_1)
            if self.answer == '3':
                quit("Выход из программы")
            elif self.answer == '1':
                self.menu_two_handler()
            else:
                self.menu_three_handler()
