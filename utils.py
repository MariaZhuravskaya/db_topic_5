import json
from typing import Any
from config import config
import psycopg2
from config import config
import requests

class DBManager:

    # Указываем адрес API для подключения в соответствующую переменную:
    API_URL = 'https://api.hh.ru/vacancies'
    # ID работодателей # Яндекс, ПАО Ростелеком, ozon и др.
    employer_id = ['9498120', '2748', '2180', '3127', '4181', '3388', '80', '4496', '9188', '1296244']

    def __init__(self, db_name='postgres'):
        self.cursor = None
        self.conn = None
        self.db_name = None
        self.params = None
        self.connect_db(db_name)

    def connect_db(self, db_name: str) -> None:
        """
        Метод для коннекта к БД
        :param db_name: имя БД
        :return: None
        """
        self.db_name = db_name
        self.params = config()
        self.params.update({'dbname': db_name})
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def get_page(self, page_number):
        """
        :param page_number: номер страницы просмотра
        :return:
        """
        params = {
            'employer_id': self.employer_id,
            'page': page_number,  # Индекс страницы поиска на HH
            'per_page': 100  # Кол-во вакансий на 1 странице
        }
        # Посылаем запрос к API
        response = requests.get(self.API_URL, params)
        # Декодируем его ответ, чтобы Кириллица отображалась корректно
        data = response.content.decode()
        # Преобразуем текст ответа запроса в справочник Python
        json_data = json.loads(data)
        return json_data

    def get_hh_data(self):
        """Получение данных о работодателях и их вакансиях по API_KEY."""

        all_vacancies = []
        first_page = self.get_page(0)
        all_vacancies.extend(first_page['items'])

        for page_number in range(1, first_page['pages']):
            page = self.get_page(page_number)
            all_vacancies.extend(page['items'])
        return all_vacancies

    def create_database(self, db_name: str) -> None:
        """Создание базы данных и таблиц для сохранения данных о работодателях и их вакансиях."""

        if self.db_name == db_name:
            self.connect_db('postgres')

        self.cursor.execute(f'DROP DATABASE IF EXISTS {db_name}')
        self.cursor.execute(f'CREATE DATABASE {db_name}')

        self.connect_db(db_name)

        self.cursor.execute("""
            CREATE TABLE employers(
            employer_id SERIAL PRIMARY KEY,
            id INTEGER,
            company_name VARCHAR(100) NOT NULL,
            url VARCHAR(100) NOT NULL
            )
            """)

        self.cursor.execute("""
                CREATE TABLE vacancies(
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                id INTEGER,
                vacancy_name VARCHAR(100) NOT NULL,
                url VARCHAR(100) NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                snippet text,
                employment VARCHAR(50),
                city VARCHAR(50)
                )
                """)

    def save_data_to_database(self, lst_all: list) -> None:
        """Сохранение данных о работодателях и их вакансиях в БД."""
        for employer in lst_all:

            if isinstance(employer['salary'], dict):
                if employer['salary']['from'] is not None:
                    employer.setdefault('from', employer['salary']['from'])
                    if employer['salary']['to'] is not None:
                        employer.setdefault('to', employer['salary']['to'])
                    else:
                        employer.setdefault('to', 0)
                else:
                    employer.setdefault('from', 0)
                    if employer['salary']['to'] is not None:
                        employer.setdefault('to', employer['salary']['to'])
                    else:
                        employer.setdefault('to', 0)
            else:
                employer.setdefault('to', 0)
                employer.setdefault('from', 0)

            if isinstance(employer['address'], dict):
                if employer['address']['city'] is not None:
                    employer.setdefault('city', employer['address']['city'])
                else:
                    employer.setdefault('city', '')
            else:
                employer.setdefault('city', '')

            id_e = employer['employer']['id']
            company_name = employer['employer']['name']
            url_employer = employer['employer']['url']

            self.cursor.execute(
                """
                INSERT INTO employers (id, company_name, url)
                VALUES (%s, %s, %s)
                RETURNING employer_id
                """,
                (id_e, company_name, url_employer)
            )

            employer_id = self.cursor.fetchone()[0]
            id_v = employer['id']
            vacancy_name = employer['name']
            url_vacancy = employer['apply_alternate_url']
            salary_from = employer['from']
            salary_to = employer['to']
            snippet = employer['snippet']['responsibility'] or ''
            employment = employer['employment']['name'] or ''
            city = employer['city']

            self.cursor.execute(
                """
                INSERT INTO vacancies (employer_id, id, vacancy_name, url, salary_from, salary_to, snippet, employment, city)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (employer_id, id_v, vacancy_name, url_vacancy, salary_from, salary_to, snippet, employment, city)
            )

    def get_companies_and_vacancies_count(self):
            """Получение списка всех компаний и количество вакансий у каждой компании."""

            self.cursor.execute(
                """
                SELECT DISTINCT e.company_name, COUNT(v.vacancy_name) as total_vacancy_company
                FROM vacancies v
                INNER JOIN employers e USING(employer_id)
                GROUP BY e.company_name
                """
            )

            result = self.cursor.fetchall()
            return result


    def get_all_vacancies(self):
        """Получение списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""

        self.cursor.execute(
            """
            SELECT e.company_name, v.vacancy_name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            INNER JOIN employers e USING(employer_id)
            """
        )
        result = self.cursor.fetchall()
        return result

    def get_avg_salary(self):
        """Получение средней зарплаты по вакансиям."""

        self.cursor.execute(
            """
            SELECT AVG(v.salary_from) AS средняя_ЗП
            FROM vacancies v
            """
        )
        result = self.cursor.fetchall()
        return result

    def get_vacancies_with_higher_salary(self):
        """Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        self.cursor.execute(
            """
            SELECT *
            FROM vacancies v
            WHERE v.salary_from > (SELECT AVG(v.salary_from) FROM vacancies v)
            ORDER BY v.salary_from
            """
        )
        result = self.cursor.fetchall()
        return result

    def get_vacancies_with_keyword(self, name: str):
        """Получение списка всех вакансий, в названии которых содержатся переданные в метод слова, например python."""

        self.cursor.execute(
            f"""
            SELECT *
            FROM vacancies v
            WHERE v.vacancy_name LIKE '%{name}%'
            """
        )
        result = self.cursor.fetchall()
        return result






