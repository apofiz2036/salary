import os
from dotenv import load_dotenv
from terminaltables import AsciiTable
import find_jobs_and_salary as find


def create_table(table, title):
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
    table.title = title
    return table.table


if __name__ == '__main__':
    secret_key = os.environ['SUPERJOB_SECRET_KEY']
    load_dotenv()

    table_hh = find.find_jobs_on_languages_hh()
    table_superjob = find.find_jobs_on_languages_superjob(secret_key)

    print(create_table(table_hh, 'HeadHunter Moscow'))
    print(create_table(secret_key, table_superjob, 'SuperJob Moscow'))
