from src.database.database import DataBase


class ClassModel:
    def __init__(self):
        self.con = DataBase()

    def get_all_classes(self):
        sql = """SELECT
                    id,
                    name
                from class"""

        students = self.con.select_all(sql)
        result = list()
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["name"] = student[1]
            result.append(data)
        return result

    def get_class(self, id):
        sql = f"""SELECT
                    s.id,
                    s.first_name,
                    s.last_name,
                    s.student_id,
                    s.class_id,
                    c.class_name,
                    s.teacher_id,
                    u.teacher_name
                FROM
                    (SELECT
                        id,
                        first_name,
                        last_name,
                        student_id,
                        teacher_id,
                        class_id
                    FROM Student where id = {id}) s
                LEFT JOIN
                    (SELECT
                        id,
                        name AS class_name
                    FROM class) c
                ON s.class_id = c.id
                LEFT JOIN
                    (SELECT
                        id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name
                    FROM user) u
                ON s.teacher_id = u.id; """

        student = self.con.select_one(sql)
        data = dict()
        data["id"] = student[0]
        data["first_name"] = student[1]
        data["last_name"] = student[2]
        data["student_id"] = student[3]
        data["class_id"] = student[4]
        data["class_name"] = student[5]
        data["teacher_id"] = student[6]
        data["teacher_name"] = student[7]
        return data

    def get_class_details(self, id):
        sql = f"""SELECT
                    c.id,
                    c.class_name,
                    u.user_id,
                    u.teacher_id,
                    u.teacher_name
                FROM
                    (SELECT
                        id,
                        name AS class_name,
                        teacher_id
                    FROM class
                    where id = '{id}') c
                LEFT JOIN
                    (SELECT
                        id as user_id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name,
                        teacher_id
                    FROM user) u
                ON u.user_id = c.teacher_id; """

        student = self.con.select_one(sql)
        data = dict()
        data["id"] = student[0]
        data["class_name"] = student[1]
        data["user_id"] = student[2]
        data["teacher_id"] = student[3]
        data["teacher_name"] = student[4]
        return data

    def check_class_exists(self, column: str, value) -> bool:
        sql = """SELECT count(*) FROM class WHERE {} ='{}' ;""".format(column, value)
        data = self.con.select_one(sql)
        if data[0] == 0:
            return False
        else:
            return True

    def add_class(self, **info) -> bool:
        try:
            if self.check_class_exists("name", info["name"]):
                return False, "Class already exists Please enter a new Class"

            self.con.insert_data("class", **info)
            return True, "Data Inserted Successfully!"

        except:  # noqa: E722
            return False, "A system error occurred, please try again later"

    def update_class(self, **info) -> bool:
        try:
            if not self.check_Student_exists("name", info["name"]):
                return False, "Class not exist"
            Id = info["id"]
            del info["id"]
            self.con.update_data("class", Id, **info)

            return True, "Update Data Successfully!"
        except:  # noqa: E722
            return False, "A system error occurred, please try again later"
