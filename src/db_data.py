sql_for_employers_create = (f'CREATE TABLE employers'
                            f'('
                            f'employer_id int PRIMARY KEY,'
                            f'employer_name varchar(250),'
                            f'open_vacancies int,'
                            f'employer_url varchar(100)'
                            f')')

sql_for_vacancies_create = (f'CREATE TABLE vacancies'
                            f'('
                            f'vacancies_id int PRIMARY KEY,'
                            f'employer_id int,'
                            f'vacancies_name varchar(250),'
                            f'vacancies_url varchar(100),'
                            f'salary_from int,'
                            f'salary_to int,'
                            f'salary_currency varchar(4)'
                            f')')
