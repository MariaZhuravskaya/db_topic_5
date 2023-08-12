Проект: Получение данных о компаниях и вакансиях с сайта hh.ru
Описание проекта
В рамках данного проекта мы получаем данные о компаниях и вакансиях с сайта hh.ru с использованием их публичного API и библиотеки requests. Затем мы проектируем таблицы в базе данных PostgreSQL для хранения полученных данных и загружаем данные в эти таблицы.

Для работы с проектом зайдите в main.py, создайте БД и заполните таблицы используя метод create_database('<имя БД>'). 


Основные шаги проекта

Получение данных с сайта hh.ru: Мы используем публичное API hh.ru и библиотеку requests для получения данных о компаниях и вакансиях.
Выбор интересующих компаний: Мы выбираем не менее 10 интересных компаний, от которых мы будем получать данные о вакансиях по API.
Проектирование таблиц в базе данных: Мы спроектируем таблицы в базе данных PostgreSQL для хранения полученных данных о компаниях и вакансиях. Для работы с базой данных мы будем использовать библиотеку psycopg2. Определим типы данных и первичный, внешние ключи.
Загрузка данных в базу данных: Мы реализуем код, который заполняет созданные таблицы в базе данных PostgreSQL данными о компаниях и вакансиях.
Создание класса DBManager: Мы создаем класс DBManager, который предоставляет методы для работы с данными в базе данных.
Класс DBManager:
import json
from typing import Any
from config import config
import psycopg2
from config import config
import requests

class DBManager:
        def __init__(self, db_name='postgres'):
        self.cursor = None
        self.conn = None
        self.db_name = None
        self.params = None
        self.connect_db(db_name)

    def connect_db(self, db_name: str) -> None:
        """Метод для коннекта к БД"""

    def get_hh_data(self):
        """Получение данных о работодателях и их вакансиях по API_KEY."""

    def create_database(self, db_name: str) -> None:
        """Создание базы данных и таблиц для сохранения данных о работодателях и их вакансиях."""

    def save_data_to_database(self, lst_all: list) -> None:
        """Сохранение данных о работодателях и их вакансиях в БД."""

    def get_companies_and_vacancies_count(self):
            """Получение списка всех компаний и количество вакансий у каждой компании."""

    def get_all_vacancies(self):
        """Получение списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""

    def get_avg_salary(self):
        """Получение средней зарплаты по вакансиям."""

    def get_vacancies_with_higher_salary(self):
        """Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""

    def get_vacancies_with_keyword(self, name: str):
        """Получение списка всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
