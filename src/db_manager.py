import os
from pprint import pprint
from typing import Any

import psycopg2
from dotenv import load_dotenv

from src.config import config


class DBManager:

    def __init__(self):
        """Конструктор класса DBManager"""
        self.__conn = None
        self.__params = config()
        self.__db_name = None

    def connect_db(self, db_name: str) -> None:
        """
        Присоединяется к БД

        :param db_name: Имя БД.
        :return:
        """
        self.__db_name = db_name
        load_dotenv()
        value = os.getenv("password_database")

        self.__conn = psycopg2.connect(
            dbname=self.__db_name, password=value, **self.__params
        )
        self.__conn.autocommit = True

    def close_connect(self) -> None:
        """Закрывает соединение с БД"""
        self.__conn.close()

    @property
    def get_conn(self) -> psycopg2.extensions.connection:
        """Геттер соединения"""
        return self.__conn

    @staticmethod
    def get_companies_and_vacancies_count(cursor: Any) -> list:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        cursor.execute(
            """
        SELECT COUNT("vacancy_name"), employee_name FROM employers GROUP BY employee_name
        """
        )

        return cursor.fetchall()

    @staticmethod
    def get_all_vacancies(cursor: Any) -> list:
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты
        и ссылки на вакансию."""
        cursor.execute(
            """
        SELECT * FROM employers
        """
        )

        return cursor.fetchall()

    @staticmethod
    def get_avg_salary(cursor: Any) -> list:
        """Получает среднюю зарплату по вакансиям."""
        cursor.execute(
            """
        SELECT AVG("salary_from"), AVG("salary_to") FROM employers
        """
        )

        return cursor.fetchall()

    @staticmethod
    def get_vacancies_with_higher_salary(cursor: Any) -> list:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        cursor.execute(
            """SELECT * FROM employers WHERE "salary_from" > (SELECT AVG("salary_from") FROM employers);
            """
        )

        return cur.fetchall()

    @staticmethod
    def get_vacancies_with_keyword(cursor: Any, word_to_find: str) -> list:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        cursor.execute(
            f"""SELECT * FROM employers WHERE vacancy_name SIMILAR TO '%({word_to_find} | {word_to_find.lower()})%';
            """
        )

        return cur.fetchall()


if __name__ == "__main__":
    manager = DBManager()
    manager.connect_db("coursework_skypro_db")
    with manager.get_conn.cursor() as cur:
        pprint(manager.get_companies_and_vacancies_count(cur))
        pprint(manager.get_all_vacancies(cur))
        pprint(manager.get_avg_salary(cur))
        pprint(manager.get_vacancies_with_higher_salary(cur))
        pprint(manager.get_vacancies_with_keyword(cur, "Менеджер"))
    manager.close_connect()
