import json
import psycopg2
from config import config


def create_database(params: dict, db_name: str) -> None:
    """Создает новую базу данных."""
pass

def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла fill_db.sql для заполнения БД данными."""
pass

def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""
pass



def get_suppliers_data(json_file: str):
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
pass


def insert_suppliers_data(cur, suppliers) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""
pass


def add_foreign_keys(cur) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
pass



