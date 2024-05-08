import requests


def job_on_languages():
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

    languages_count = dict()
    url = 'https://api.hh.ru/'
    
    for language in languages:
        payload = {
            'text': f'программист {language}',
            'area': '1',
            'period': '30'
        }
        response = requests.get(f'{url}vacancies', params=payload)
        response.raise_for_status()
        vacancies = response.json()['found']
        languages_count[language] = vacancies
    print(languages_count)


def predict_rub_salary(vacancy):
    url = 'https://api.hh.ru/'
    payload = {
        'text': vacancy,
        'area': '1',
        'period': '30',
    }
    response = requests.get(f'{url}vacancies', params=payload)
    response.raise_for_status
    vacancies = response.json()['items']

    for salary in vacancies:
        salary = salary['salary']
        if salary is None:
            print(None)
        elif salary['currency'] != 'RUR':
            print(None)
        elif (salary['from'] is not None) and (salary['to'] is not None):
            print((salary['from']+salary['to'])/2)
        else:
            print(salary['from'])


job_on_languages()
