from src.database.database import DataBase


class SubjectModel:
    def __init__(self):
        self.con = DataBase()

    def get_all_subjects_by_class_id(self, id):
        sql = f"""SELECT
                    s.id,
                    s.name,
                    c.class_id,
                    c.class_name,
                    t.tech_id,
                    t.teacher_id,
                    t.teacher_name
                FROM
                    (SELECT
                        id,
                        name,
                        teacher_id,
                        class_id
                    FROM Subject
                    where class_id = '{id}') s
                LEFT JOIN
                    (SELECT
                        id as class_id,
                        name AS class_name
                    FROM class) c
                ON s.class_id = c.class_id
                LEFT JOIN
                    (SELECT
                        id as tech_id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name,
                        teacher_id
                    FROM Teacher) t
                ON s.teacher_id = t.tech_id;"""

        students = self.con.select_all(sql)
        result = list()
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["name"] = student[1]
            data["class_id"] = student[2]
            data["class_name"] = student[3]
            data["tech_id"] = student[4]
            data["teacher_id"] = student[5]
            data["teacher_name"] = student[6]
            result.append(data)
        return result

    def get_all_subjects_by_teacher_id(self, id):
        sql = f"""SELECT
                    s.id,
                    s.name,
                    c.class_id,
                    c.class_name,
                    t.tech_id,
                    t.teacher_id,
                    t.teacher_name
                FROM
                    (SELECT
                        id,
                        name,
                        teacher_id,
                        class_id
                    FROM Subject
                    where teacher_id = '{id}') s
                LEFT JOIN
                    (SELECT
                        id as class_id,
                        name AS class_name
                    FROM class) c
                ON s.class_id = c.class_id
                LEFT JOIN
                    (SELECT
                        id as tech_id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name,
                        teacher_id
                    FROM Teacher) t
                ON s.teacher_id = t.tech_id;"""

        students = self.con.select_all(sql)
        result = list()
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["name"] = student[1]
            data["class_id"] = student[2]
            data["class_name"] = student[3]
            data["tech_id"] = student[4]
            data["teacher_id"] = student[5]
            data["teacher_name"] = student[6]
            result.append(data)
        return result

    def get_all_subjects(self):
        sql = """SELECT
                    s.id,
                    s.name,
                    c.class_id,
                    c.class_name,
                    t.teach_id,
                    t.teacher_id,
                    t.teacher_name
                FROM
                    (SELECT
                        id,
                        name,
                        teacher_id,
                        class_id
                    FROM Subject) s
                LEFT JOIN
                    (SELECT
                        id as class_id,
                        name AS class_name
                    FROM class) c
                ON s.class_id = c.class_id
                LEFT JOIN
                    (SELECT
                        id as teach_id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name,
                        teacher_id
                    FROM Teacher) t
                ON s.teacher_id = t.teach_id;"""

        students = self.con.select_all(sql)
        result = list()
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["name"] = student[1]
            data["class_id"] = student[2]
            data["class_name"] = student[3]
            data["teach_id"] = student[4]
            data["teacher_id"] = student[5]
            data["teacher_name"] = student[6]
            result.append(data)
        return result

    def get_subject(self, id):
        sql = f"""SELECT
                    s.id,
                    s.name,
                    c.class_id,
                    c.class_name,
                    t.tech_id,
                    t.teacher_name
                FROM
                    (SELECT
                        id,
                        name,
                        teacher_id,
                        class_id
                    FROM Subject
                    where id = '{id}') s
                LEFT JOIN
                    (SELECT
                        id as class_id,
                        name AS class_name
                    FROM class) c
                ON s.class_id = c.class_id
                LEFT JOIN
                    (SELECT
                        id as tech_id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name,
                        teacher_id
                    FROM Teacher) t
                ON s.teacher_id = t.tech_id;"""

        student = self.con.select_one(sql)
        data = dict()
        data["id"] = student[0]
        data["name"] = student[1]
        data["class_id"] = student[2]
        data["class_name"] = student[3]
        data["teacher_id"] = student[4]
        data["teacher_name"] = student[5]
        return data

    def check_subject_exists(self, column: str, value) -> bool:
        sql = """SELECT count(*) FROM subject WHERE {} ='{}' ;""".format(column, value)
        data = self.con.select_one(sql)
        if data[0] == 0:
            return False
        else:
            return True

    def add_subject(self, **info) -> bool:
        try:
            # if self.check_subject_exists("name", info["name"]):
            #     return False, "Subject already exists Please enter a new Subject"

            self.con.insert_data("subject", **info)
            return True, "Data Inserted Successfully!"

        except:  # noqa: E722
            return False, "A system error occurred, please try again later"

    def update_subject(self, **info) -> bool:
        try:
            if not self.check_subject_exists("name", info["name"]):
                return False, "Subject not exist"
            Id = info["id"]
            del info["id"]
            self.con.update_data("subject", Id, **info)

            return True, "Update Data Successfully!"
        except:  # noqa: E722
            return False, "A system error occurred, please try again later"
