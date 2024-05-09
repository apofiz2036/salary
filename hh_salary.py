import requests
from pprint import pprint


def job_on_languages():
    jobs_on_languages = dict()
    languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C',
        'Go',
        'Shell']

    url = 'https://api.hh.ru/'

    for language in languages:
        job_and_salary = dict()
        payload = {
            'text': f'программист {language}',
            'area': '1',
            'period': '30'
        }
        response = requests.get(f'{url}vacancies', params=payload)
        response.raise_for_status()
        vacancies_found = response.json()['found']
        job_and_salary['vacancies_found'] = vacancies_found

        vacancies_salary = response.json()['items']
        salaries = []
        for salary in vacancies_salary:
            salary = salary['salary']
            if salary is None:
                continue
            elif salary['currency'] != 'RUR':
                continue
            elif (salary['from'] is not None) and (salary['to'] is not None):
                salaries.append((salary['from']+salary['to'])/2)
            else:
                if salary['from'] is not None:
                    salaries.append(salary['from'])
            job_and_salary['vacancies_processed'] = len(salaries)

            if salaries:
                job_and_salary['average_salary'] = int(sum(salaries)/len(salaries))
            else:
                job_and_salary['average_salary'] = 0

        jobs_on_languages[language] = job_and_salary

    return jobs_on_languages


def pages(language):
    url = 'https://api.hh.ru/vacancies'
    vacancies = []
    page = 0
    pages_number = 1

    while page < pages_number:
        payload = {
                'text': f'программист {language}',
                'area': '1',
                'period': '30',
                'page': page
            }
        response = requests.get(url, params=payload)
        response.raise_for_status()

        vacancies_from_page = response.json()
        vacancies.extend(vacancies_from_page['items'])
        pages_number = vacancies_from_page['pages']
        page += 1

    return len(vacancies)

# pprint(job_on_languages())
print(pages('python'))
