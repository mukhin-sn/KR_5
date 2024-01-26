from configparser import ConfigParser


def config(filename='database.ini', section='postgresql') -> dict:
    """
    Метод чтения конфигурации для соединения с базой данных из файла
    :param filename: имя файла конфигурации
    :param section: секция в файле, которую необходимо прочитать
    :return: словарь параметров для соединения с базой данных
    """

    # Создаем парсер
    parser = ConfigParser()

    # Читаем конфигурацию из секции файла
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} is not found in the {filename} file')
    return db
