# Сравниваем вакансии программистов

Данная программа позволяет загружать с сайтов информацию о вакансиях и оформлять их в виде таблицы. В таблице указывается язык программирования, количество обнаруженных вакансий, количество обработанных вакансий(вакансии в которых указана заработная плата) и средняя зарплата по этим вакансиям.

## Установка
Для работы программы требуется  Python 3.6 или выше, библиотека requests версии 2.31.0, библиотека python-dotenv версии 1.0.1 и библиотека terminaltables версии 3.1.10.  Все необходимые для работы библиотеки прописаны в файле requirements.txt, установить их можно с помощью комманды:

```shell
 pip install -r requirements.txt.
```

Для работы требуется указать sekret key с сайта [superjob.ru](https://www.superjob.ru/). Прописать ключ нужно в файле .env следующим образом:

```.env
SUPERJOB_SECRET_KEY==ваш ключ
```
## Использование

Для работы программы требуется прописать следующую команду в консоли:

```shell
python jobs_and_salary_table.py
```

Дополнительные параметры не требуются.

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).