from src.database.database import DataBase


class TermsModel:
    def __init__(self):
        self.con = DataBase()

    def get_all_terms(self):
        sql = """SELECT
                    id,
                    name
                    from terms order by name asc;"""

        students = self.con.select_all(sql)
        result = list()
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["name"] = student[1]
            result.append(data)
        return result
