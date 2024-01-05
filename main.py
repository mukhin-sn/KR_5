from src.hh_areas import get_areas
from test import get_employers, get_vacancies


def main():

    # Тестирование функции get_employers()
    # ===============================================
    # emplr = 'Газпром'
    # get_employers(emplr)

    # get_employers('')
    # print('-' * 300 + "\n")
    # ===============================================

    # Тестирование функции get_vacancies()
    # ===============================================
    # txt = "Python"
    # employers_id = '49357'  # '1455'
    # areas = 113
    # vacan = get_vacancies(txt, employers_id, areas)
    # print(vacan[0])
    # for i in vacan[1]:
    #     print(i)
    # ===============================================

    # Тестирование функции get_areas()
    # ===============================================
    areas = get_areas()
    print(len(areas))
    for ar in areas:
        print(ar)
    # ===============================================



if __name__ == '__main__':
    main()

