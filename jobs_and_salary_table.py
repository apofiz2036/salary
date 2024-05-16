import os
from terminaltables import AsciiTable
import find_jobs_and_salary as find


def create_table_superjob(table):
    table_rows = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]

    for language, vacancies in table().items():
        table_rows.append([
            language,
            vacancies["vacancies_found"],
            vacancies["vacancies_processed"],
            vacancies["average_salary"]
        ])

    table = AsciiTable(table_rows)
    table.title = 'SuperJob Moscow'
    return table.table


def create_table_hh(table):
    table_rows = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]

    for language, vacancies in table.items():
        table_rows.append([
            language,
            vacancies["vacancies_found"],
            vacancies["vacancies_processed"],
            vacancies["average_salary"]
        ])

    table = AsciiTable(table_rows)
    table.title = 'HeadHunter Moscow'
    return table.table


if __name__ == '__main__':
    secret_key = os.environ['SUPERJOB_SECRET_KEY']

    table_hh = find.find_jobs_on_languages_hh()
    table_superjob = find.find_jobs_on_languages_superjob(secret_key)

    print(create_table_hh(table_hh))
    print(create_table_superjob(secret_key, table_superjob))
