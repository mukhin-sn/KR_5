from src.db_class import DBManager
from src.hh_class import HhClass, EmployersHhClass


class MenuHandler:
    """
    Класс для работы с меню программы
    """

    def __init__(self, db_obj: DBManager, vacancies_object: HhClass, employers_object: EmployersHhClass):

        # Главное меню программы
        self.menu_1 = {'1': 'Работа с запросами к сайту hh.ru',
                       '2': 'Работа с базой данных',
                       '3': 'Выход из программы',
                       }

        # Меню работы с запросами к сайту hh.ru
        self.menu_2 = {'1': 'Поиск работодателей по ключевым словам',
                       '2': 'Поиск работодателей по ID',
                       '3': 'Выход в главное меню',
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
        self.vacancies_object = vacancies_object
        self.employers_object = employers_object
        self.db_obj = db_obj
        self.file_employers_id = 'file_employers_id.json'
        self.hi_message = ('Введите поисковый запрос:\n'
                           'Слова, которые должны быть в названии вакансии, '
                           'перечислите через запятую')
        self.any_key = ''

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

    def save_vacancies_to_db(self, emp_list: list[tuple]):
        """
        Метод формирования таблицы vacancies в базе данных
        :param emp_list: список для передачи в базу данных
        :return:
        """
        print(f'После сохранения работодателей в базу,\n'
              f'будет формироваться таблица вакансий по этим работодателям,\n'
              f'Это может занять длительное время')
        answer = self.second_menu('Сохранить найденных работодателей в базу данных?')
        if answer == '1':
            self.db_obj.load_to_db('employers', emp_list)

            # После сохранения данных по работодателям в базу данных
            # будет сформирована таблица вакансий для этих работодателей
            # Максимальное количество вакансий ограничено 2000

            # Получим список ID работодателей из списка работодателей
            emp_id_list = []
            for emp_id in emp_list:
                emp_id_list.append(emp_id[0])
            for id_ in emp_id_list:
                out_list = self.vacancies_object.get_data(employer_id=id_)
                self.db_obj.load_to_db('vacancies', out_list)

    def menu_three_handler(self):
        """
        Метод обработки меню работы с базой данных
        """
        while True:
            self.answer = self.print_menu(self.menu_3)
            if self.answer == '6':
                break
            elif self.answer == '1':
                out_data = self.db_obj.get_companies_and_vacancies_count()
                self.db_obj.print_data_db(out_data)
            elif self.answer == '2':
                out_data = self.db_obj.get_all_vacancies()
                self.db_obj.print_data_db(out_data)
            elif self.answer == '3':
                out_data = self.db_obj.get_avg_salary()
                self.out_message(f'Средняя зарплата по вакансиям составляет:\n{out_data}')
            elif self.answer == '4':
                out_data = self.db_obj.get_vacancies_with_higher_salary()
                self.db_obj.print_data_db(out_data)
            else:
                self.out_message(self.hi_message)
                answer = self.input_answer()
                out_data = self.db_obj.get_vacancies_with_keyword(answer)
                self.db_obj.print_data_db(out_data)

    def menu_two_handler(self):
        """
        Метод обработки меню работы с запросами к сайту hh.ru
        """
        # Список, для записи в базу данных
        emp_list = []
        while True:
            self.answer = self.print_menu(self.menu_2)
            if self.answer == '3':
                break

            # Поиск работодателей по ключевым словам
            elif self.answer == '1':
                emp_list.clear()
                self.out_message(self.hi_message)
                answer = self.input_answer()
                self.out_message('Ожидайте, обработка запроса займёт некоторое время')
                answer = HhClass.get_text(answer)
                self.vacancies_object.params['text'] = f'NAME:{answer}'
                vac_list = self.vacancies_object.get_data(**self.vacancies_object.params)
                self.vacancies_object.print_data_list()
                self.any_key = input('Для продолжения нажмите "Enter"')
                self.out_message(f'Список ID - компаний, содержащих '
                                 f'ключевые слова,\nбудет сохранен в файл '
                                 f'{self.file_employers_id}')
                emp_id_list = self.employers_object.id_employers_filter(vac_list)
                HhClass.save_to_file(self.file_employers_id, emp_id_list)
                self.out_message('Ожидайте, формирование списка работодателей займёт некоторое время')

                # выделяем отсутствующих в базе данных работодателей из полученного списка ID работодателей
                emp_id_list = self.db_obj.check_id_employers(emp_id_list)
                for emp_id in emp_id_list:
                    self.employers_object.employer_id = emp_id
                    dt = self.employers_object.get_data()[0]
                    print(dt)
                    emp_list.append(dt)

                # Формируем таблицу Vacancies
                self.save_vacancies_to_db(emp_list)

            # Поиск работодателей по ID
            else:
                emp_list.clear()
                self.out_message('Введите ID - работодателей через запятую')
                answer = self.input_answer()
                emp_id_list = HhClass.get_list_id(answer)
                if not emp_id_list:
                    self.out_message('В веденных данных нет ID.\nПопробуйте ещё раз.')
                    continue
                for emp_id in emp_id_list:
                    self.employers_object.employer_id = emp_id
                    try:
                        emp_list.append(self.employers_object.get_data()[0])
                    except:
                        self.out_message(f'Работодатель с ID {emp_id} не найден')
                        continue
                # Если не найден ни один работодатель
                if not emp_list:
                    print('Для введенных ID отсутствуют сведения о работодателях')
                    continue
                # Формируем таблицу Vacancies
                self.save_vacancies_to_db(emp_list)

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

    def second_menu(self, message):
        self.out_message(message)
        return self.print_menu(self.answers_list)
