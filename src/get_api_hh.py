from copy import copy

import requests


class GetHhAPI:

    @staticmethod
    def get_employer_info(employer_id: str) -> list:
        """Получает информацию о работодателе по его id. Учитываются вакансии, где указан
        верхний или нижний порог зарплаты"""
        data = []
        url = "https://api.hh.ru/vacancies"
        params = {"employer_id": employer_id, "per_page": 100, "only_with_salary": True}
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            data = response.json()["items"]

        return data

    @staticmethod
    def set_data_to_list(data: list) -> list[dict]:
        """Помещает данные по одному работодателю в список словарей"""
        struct: dict = {
            "employee_name": None,
            "vacancy_name": None,
            "salary_from": None,
            "salary_to": None,
            "area": None,
        }
        result: list = []
        for element in data:
            struct = copy(struct)
            struct["employee_name"] = element["employer"]["name"]
            struct["vacancy_name"] = element["name"]
            struct["salary_from"] = element["salary"]["from"]
            struct["salary_to"] = element["salary"]["to"]
            struct["area"] = element["area"]["name"]
            result.append(struct)
        return result


# id_of_companies_list = ["988387", "3809", "3388", "4219", "15478", "3127", "80", "1942336", "132654", "1942330"]
#
# for e in id_of_companies_list:
#     print(GetHhAPI.set_data_to_list(GetHhAPI.get_employer_info(e)))
