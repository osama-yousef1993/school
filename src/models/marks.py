from uuid import uuid4

from src.database.database import DataBase


class MarksModel:
    def __init__(self):
        self.con = DataBase()

    def get_all_marks(self):
        sql = """SELECT
                    s.id,
                    s.participation,
                    s.home_work,
                    s.class_work,
                    s.quiz,
                    s.mid_term,
                    s.final,
                    s.student_id,
                    s.teacher_id,
                    c.name,
                    u.teacher_name
                FROM
                    (SELECT
                        id,
                        participation,
                        home_work,
                        class_work,
                        quiz,
                        mid_term,
                        final,
                        teacher_id,
                        student_id
                    FROM Marks) s
                LEFT JOIN
                    (SELECT
                        id,
                        concat(first_name, ' ', last_name) AS name,
                        student_id
                    FROM Student) c
                ON s.student_id = c.id
                LEFT JOIN
                    (SELECT
                        id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name,
                        teacher_id
                    FROM user) u
                ON s.teacher_id = u.id; """

        students = self.con.select_all(sql)
        result = list()
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["participation"] = student[1]
            data["home_work"] = student[2]
            data["class_work"] = student[3]
            data["quiz"] = student[4]
            data["mid_term"] = student[5]
            data["final"] = student[6]
            data["student_id"] = student[7]
            data["teacher_id"] = student[8]
            data["student_name"] = student[9]
            data["teacher_name"] = student[10]
            result.append(data)
        return result

    def get_student_marks(self, student_id, subject_id):
        sql = f"""SELECT
                    s.id,
                    s.participation,
                    s.home_work,
                    s.class_work,
                    s.quiz,
                    s.mid_term,
                    s.final,
                    c.student_id,
                    c.student_name,
                    s.subject_id,
                    su.subject_name,
                    s.class_id,
                    cl.class_name,
                    u.teacher_id,
                    u.teacher_name,
                    mt.term_id,
                    mt.id as mark_term_id,
                    t.term_name
                FROM
                    (SELECT
                        id,
                        participation,
                        home_work,
                        class_work,
                        quiz,
                        mid_term,
                        final,
                        teacher_id,
                        student_id,
                        subject_id,
                        class_id
                    FROM Marks
                    WHERE student_id = '{student_id}'
                    AND subject_id ='{subject_id}') s
                LEFT JOIN
                    (SELECT
                        id,
                        concat(first_name, ' ', last_name) AS student_name,
                        student_id
                    FROM Student) c
                ON s.student_id = c.id
                LEFT JOIN
                    (SELECT
                        id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name,
                        teacher_id
                    FROM Teacher) u
                ON s.teacher_id = u.id
                LEFT JOIN
                    (SELECT
                        id,
                        name AS subject_name
                    FROM Subject) su
                ON s.subject_id = su.id
                LEFT JOIN
                    (SELECT
                        id,
                        name AS class_name
                    FROM Class) cl
                ON s.class_id = cl.id
                LEFT JOIN
                    term_marks mt
                ON s.id = mt.mark_id
                LEFT JOIN
                    (SELECT
                        id as term_id,
                        name as term_name
                    FROM Terms) t
                ON mt.term_id = t.term_id
                ;"""

        students = self.con.select_all(sql)
        result = list()
        for student in students:
            data = dict()
            if student:
                data["id"] = student[0]
                data["participation"] = student[1]
                data["home_work"] = student[2]
                data["class_work"] = student[3]
                data["quiz"] = student[4]
                data["mid_term"] = student[5]
                data["final"] = student[6]
                data["student_id"] = student[7]
                data["student_name"] = student[8]
                data["subject_id"] = student[9]
                data["subject_name"] = student[10]
                data["class_id"] = student[11]
                data["class_name"] = student[12]
                data["teacher_id"] = student[13]
                data["teacher_name"] = student[14]
                data["term_id"] = student[15]
                data["mark_term_id"] = student[16]
                data["term_name"] = student[17]
                result.append(data)

        return result

    def check_mark_exists(self, column: str, value) -> bool:
        sql = """SELECT count(*) FROM Marks WHERE {} ='{}' ;""".format(column, value)
        data = self.con.select_one(sql)
        if data[0] == 0:
            return False
        else:
            return True

    def check_mark_terms_exists(self, column: str, value) -> bool:
        sql = """SELECT count(*) FROM term_marks WHERE {} ='{}' ;""".format(
            column, value
        )
        data = self.con.select_one(sql)
        if data is None or data[0] == 0:
            return False
        else:
            return True

    def add_mark(self, **info) -> bool:
        try:
            mark_term_id = info["mark_term_id"]
            terms_id = info["terms_id"]
            del info["terms_id"]
            del info["mark_term_id"]
            self.con.upsert_data("marks", **info)
            if mark_term_id == "":
                data = dict()
                data["id"] = str(uuid4())
                data["term_id"] = terms_id
                data["mark_id"] = info["id"]
                self.con.insert_data("term_marks", **data)
            return True, "Data Inserted Successfully!"

        except Exception as e:  # noqa: E722
            print("error:=> ", e)
            return False, "A system error occurred, please try again later"

    def update_mark(self, **info) -> bool:
        try:
            if not self.check_mark_exists("id", info["id"]):
                return False, "Student Id not exist"
            Id = info["id"]
            del info["id"]
            self.con.update_data("marks", Id, **info)

            return True, "Update Data Successfully!"
        except:  # noqa: E722
            return False, "A system error occurred, please try again later"
