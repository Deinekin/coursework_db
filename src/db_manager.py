from pprint import pprint
from typing import Any

import psycopg2

from src.config import config


class DBManager:
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
    params = config()
    manager = DBManager()
    conn = psycopg2.connect(dbname="coursework_skypro_db", **params)
    cur = conn.cursor()
    pprint(manager.get_companies_and_vacancies_count(cur))
    pprint(manager.get_all_vacancies(cur))
    pprint(manager.get_avg_salary(cur))
    pprint(manager.get_vacancies_with_higher_salary(cur))
    pprint(manager.get_vacancies_with_keyword(cur, "Менеджер"))
