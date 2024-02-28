from src.db_manager import DBManager
from src.get_api_hh import GetHhAPI


class AddDataToDB:

    @staticmethod
    def add_all_data_to_list() -> list[dict]:
        """Помещает все данные о вакансиях и работодателях в список словарей"""
        list_of_all_vacancies: list = []
        id_of_companies_list: list = [
            "988387",
            "3809",
            "3388",
            "4219",
            "15478",
            "3127",
            "80",
            "1942336",
            "132654",
            "1942330",
        ]
        result: list = []
        employer_info = GetHhAPI()
        for element in id_of_companies_list:
            list_of_all_vacancies.append(
                GetHhAPI.set_data_to_list(employer_info.get_employer_info(element))
            )

        for element in list_of_all_vacancies:
            for dict_ in element:
                result.append(dict_)
        return result

    @staticmethod
    def set_data_to_db(table_name: str) -> None:
        """Записывает данные в базу данных"""
        manager = DBManager()
        manager.connect_db("coursework_skypro_db")

        with manager.get_conn.cursor() as cur:
            for element in AddDataToDB.add_all_data_to_list():
                cur.execute(
                    f"""
                INSERT INTO {table_name} (employee_name, vacancy_name, salary_from, salary_to, area)
                VALUES (%s, %s, %s, %s, %s)
                """,
                    (
                        element["employee_name"],
                        element["vacancy_name"],
                        element["salary_from"],
                        element["salary_to"],
                        element["area"],
                    ),
                )
        cur.close()
        manager.close_connect()


# AddDataToDB.set_data_to_db("employers")
