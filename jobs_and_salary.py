import requests
import os
from terminaltables import AsciiTable
from dotenv import load_dotenv


def find_superjob_vacancy_moscow():
    columns_in_table = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]

    for language, vacancies in find_jobs_on_languages_superjob().items():
        columns_in_table.append([
            language,
            vacancies["vacancies_found"],
            vacancies["vacancies_processed"],
            vacancies["average_salary"]
        ])

    table = AsciiTable(columns_in_table)
    table.title = 'SuperJob Moscow'
    print(table.table)


def find_headhunter_vacancy_moscow():
    columns_in_table = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]

    for language, vacancies in find_jobs_on_languages_hh().items():
        columns_in_table.append([
            language,
            vacancies["vacancies_found"],
            vacancies["vacancies_processed"],
            vacancies["average_salary"]
        ])

    table = AsciiTable(columns_in_table)
    table.title = 'HeadHunter Moscow'
    print(table.table)


def find_jobs_on_languages_hh():
    jobs_on_languages_hh = dict()
    languages = [
        'JavaScript',
        'Java',
        'Python',
    ]

    for language in languages:
        job_and_salary = dict()
        url = 'https://api.hh.ru/vacancies'
        vacancies_found = 0
        salaries = []
        page = 0

        while True:
            payload = {
                'text': f'программист {language}',
                'area': '1',
                'period': '30',
                'per_page': 100,
                'page': page
            }
            response = requests.get(f'{url}', params=payload)
            response.raise_for_status()

            vacancies_from_page = response.json()['items']
            vacancies_found += len(vacancies_from_page)

            for vacancy in vacancies_from_page:
                salary = vacancy.get('salary')
                if salary is None:
                    continue
                elif salary['currency'] != 'RUR':
                    continue
                elif (salary['from'] is not None) and (salary['to'] is not None):
                    salaries.append((salary['from']+salary['to'])/2)
                else:
                    if salary['from'] is not None:
                        salaries.append(salary['from'])

            if response.json()['pages'] == page + 1:
                break

            page += 1

        job_and_salary['vacancies_found'] = vacancies_found
        job_and_salary['vacancies_processed'] = len(salaries)

        if salaries:
            job_and_salary['average_salary'] = int(
                sum(salaries) / len(salaries))
        else:
            job_and_salary['average_salary'] = 0

        jobs_on_languages_hh[language] = job_and_salary

    return jobs_on_languages_hh


def find_jobs_on_languages_superjob():
    load_dotenv()
    jobs_on_languages_superjob = dict()
    languages = [
        'JavaScript',
        'Java',
        'Python',
    ]
    secret_key = os.environ['SUPERJOB_SECRET_KEY']

    for language in languages:
        url = '	https://api.superjob.ru/2.0/vacancies/'
        page = 0
        vacancies_processed = 0
        vacancies_found = 0
        salaries = []

        while True:
            payload = {
                'town': 4,
                'catalogues': 48,
                'keyword': language,
                'count': 100,
                'page': page
            }
            headers = {
                'X-Api-App-Id': secret_key
            }
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()

            vacancies_from_page = response.json()['objects']
            vacancies_found += len(vacancies_from_page)

            if not vacancies_from_page:
                break

            for vacancy in vacancies_from_page:
                vacancies_processed += 1
                salary = predict_rub_salary_for_superJob(vacancy)
                if salary is not None:
                    salaries.append(salary)

            page += 1

        if salaries:
            average_salary = sum(salaries) / len(salaries)
        else:
            average_salary = 0

        jobs_on_languages_superjob[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary
        }

    return jobs_on_languages_superjob


def predict_rub_salary_for_superJob(vacancy):
    if vacancy['payment_from'] == 0:
        return None
    elif vacancy['payment_from'] != 0 and vacancy['payment_to'] != 0:
        return ((vacancy['payment_from']+vacancy['payment_to'])/2)
    else:
        return vacancy['payment_from']


if __name__ == '__main__':
    find_superjob_vacancy_moscow()
    find_headhunter_vacancy_moscow()
