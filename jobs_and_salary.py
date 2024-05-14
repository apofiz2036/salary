import requests
import os
from terminaltables import AsciiTable
from dotenv import load_dotenv


def find_superjob_vacancy_moscow(jobs_on_languages_superjob):
    columns_in_table = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]
    
    for language, vacancies in jobs_on_languages_superjob().items():
        columns_in_table.append([
            language,
            vacancies["vacancies_found"],
            vacancies["vacancies_processed"],
            vacancies["average_salary"]
        ])

    table = AsciiTable(columns_in_table)
    table.title = 'SuperJob Moscow'
    print(table.table)


def find_headhunter_vacancy_moscow(jobs_on_languages_hh):
    columns_in_table = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]

    for language, vacancies in jobs_on_languages_hh.items():
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
        url = 'https://api.hh.ru/vacancies'
        vacancies_found = 0
        salaries = []
        page = 0
        moscow_area_id = 1
        days_period = 30
        vacancies_per_page = 100

        while True:
            payload = {
                'text': f'программист {language}',
                'area': moscow_area_id,
                'period': days_period,
                'per_page': vacancies_per_page,
                'page': page
            }
            response = requests.get(f'{url}', params=payload)
            response.raise_for_status()

            vacancies_from_page = response.json()
            vacancies_found = vacancies_from_page['found']

            for vacancy in vacancies_from_page['items']:
                salary = vacancy.get('salary')
                if not salary:
                    continue
                elif salary['currency'] != 'RUR':
                    continue
                elif salary['from'] and salary['to']:
                    salaries.append((salary['from']+salary['to'])/2)
                elif salary['from'] and not salary['to']:
                    salaries.append(salary['from']*1.2)
                elif not salary['from'] and salary['to']:
                    salaries.append(salary['to']*0.8)

            if vacancies_from_page['pages'] == page + 1:
                break

            page += 1

        job_and_salary = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(salaries)
        }

        if salaries:
            job_and_salary['average_salary'] = int(
                sum(salaries) / len(salaries))
        else:
            job_and_salary['average_salary'] = 0

        jobs_on_languages_hh[language] = job_and_salary

    return jobs_on_languages_hh


def find_jobs_on_languages_superjob(secret_key):
    jobs_on_languages_superjob = dict()
    languages = [
        'JavaScript',
        'Java',
        'Python',
    ]

    for language in languages:
        url = '	https://api.superjob.ru/2.0/vacancies/'
        page = 0
        moscow_town_id = 4
        it_vacancy_category = 48
        vacancies_per_page = 100
        vacancies_processed = 0
        vacancies_found = 0
        salaries = []

        while True:
            payload = {
                'town': moscow_town_id,
                'catalogues': it_vacancy_category,
                'keyword': language,
                'count': vacancies_per_page,
                'page': page
            }
            headers = {
                'X-Api-App-Id': secret_key
            }
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()

            vacancies_response = response.json()
            vacancies_from_page = vacancies_response['objects']
            vacancies_found = vacancies_response['found']

            if not vacancies_from_page:
                break

            for vacancy in vacancies_from_page:
                vacancies_processed += 1
                salary = predict_rub_salary_for_superJob(vacancy)
                if not salary:
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
    if vacancy['payment_from'] and vacancy['payment_to']:
        return (vacancy['payment_from']+vacancy['payment_to'])/2
    elif not vacancy['payment_from'] and vacancy['payment_to']:
        return vacancy['payment_to']*0.8
    elif vacancy['payment_from'] and not vacancy['payment_to']:
        return vacancy['payment_from']*1.2


if __name__ == '__main__':
    load_dotenv()
    secret_key = os.environ['SUPERJOB_SECRET_KEY']
    # jobs_on_languages_superjob = find_jobs_on_languages_superjob(secret_key)
    # find_superjob_vacancy_moscow(jobs_on_languages_superjob)
    jobs_on_languages_hh = find_jobs_on_languages_hh()
    find_headhunter_vacancy_moscow(jobs_on_languages_hh)
