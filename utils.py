import json
from config import config
import psycopg2
from config import config
import requests

class DBManager:

    def __init__(self, database_name):
        self.params = config()
        self.params.update({'dbname': database_name})
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def get_hh_data(self, api_key: str):
        """Получение данных о работодателях и их вакансиях по API_KEY."""



    def create_database(self, params: dict, db_name: str) -> None:
        """Создание базы данных и таблиц для сохранения данных о работодателях и их вакансиях."""
        pass

    def save_data_to_database(self, cur) -> None:
        """Сохранение данных о работодателях и их вакансиях в БД."""
        pass

    def get_companies_and_vacancies_count(self, db_name: str):
        """Получение списка всех компаний и количество вакансий у каждой компании."""
        pass

    def get_all_vacancies(self, db_name: str):
        """Получение списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        pass

    def get_avg_salary(self, db_name: str):
        """Получение средней зарплаты по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self, db_name: str):
        """Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self, db_name: str):
        """Получение списка всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        pass



