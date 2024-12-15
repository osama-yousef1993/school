from uuid import uuid4

from src.database.database import DataBase


class StudentModel:
    def __init__(self):
        self.con = DataBase()

    def get_all_students(self):
        sql = """SELECT
                    s.id,
                    s.first_name,
                    s.last_name,
                    s.student_id,
                    s.class_id,
                    c.class_name,
                    u.teacher_id,
                    u.teacher_name
                FROM
                    (SELECT
                        id,
                        first_name,
                        last_name,
                        student_id,
                        teacher_id,
                        class_id
                    FROM Student) s
                LEFT JOIN
                    (SELECT
                        id,
                        name AS class_name
                    FROM class) c
                ON s.class_id = c.id
                LEFT JOIN
                    (SELECT
                        id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name,
                        teacher_id
                    FROM teacher) u
                ON s.teacher_id = u.id; """

        students = self.con.select_all(sql)
        result = list()
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["first_name"] = student[1]
            data["last_name"] = student[2]
            data["student_id"] = student[3]
            data["class_id"] = student[4]
            data["class_name"] = student[5]
            data["teacher_id"] = student[6]
            data["teacher_name"] = student[7]
            result.append(data)
        return result

    def get_all_students_by_class_id(self, id):
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
                    FROM Student) s
                LEFT JOIN
                    (SELECT
                        id,
                        name AS class_name,
                        teacher_id
                    FROM class where id = '{id}') c
                ON s.class_id = c.id
                LEFT JOIN
                    (SELECT
                        id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name
                    FROM teacher) u
                ON c.teacher_id = u.id; """

        students = self.con.select_all(sql)
        result = list()
        print(students)
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["first_name"] = student[1]
            data["last_name"] = student[2]
            data["student_id"] = student[3]
            data["class_id"] = student[4]
            data["class_name"] = student[5]
            data["teacher_id"] = student[6]
            data["teacher_name"] = student[7]
            result.append(data)
        return result

    def get_all_students_by_subject_id(self, id):
        sql = f"""SELECT
                    s.id,
                    s.first_name,
                    s.last_name,
                    s.student_id,
                    s.class_id,
                    c.class_name,
                    t.teacher_id,
                    t.teacher_name,
                    su.subject_id,
                    su.subject_name
                FROM
                    (SELECT
                        id,
                        first_name,
                        last_name,
                        student_id,
                        teacher_id,
                        class_id,
                        subject_id
                    FROM Student
                    WHERE subject_id = '{id}') s
                LEFT JOIN
                    (SELECT
                        id,
                        name AS class_name
                    FROM class) c
                ON s.class_id = c.id
                LEFT JOIN
                    (SELECT
                        id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name,
                        teacher_id
                    FROM teacher) t
                ON s.teacher_id = t.id
                LEFT JOIN
                (SELECT
                    id as subject_id,
                    name as subject_name,
                    class_id
                FROM subject
                WHERE id = '{id}') su
                ON su.class_id = s.class_id"""

        students = self.con.select_all(sql)
        result = list()
        print(students)
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["first_name"] = student[1]
            data["last_name"] = student[2]
            data["student_id"] = student[3]
            data["class_id"] = student[4]
            data["class_name"] = student[5]
            data["teacher_id"] = student[6]
            data["teacher_name"] = student[7]
            data["subject_id"] = student[8]
            data["subject_name"] = student[9]
            result.append(data)
        return result

    def get_all_students_by_teacher_id(self, ids):
        subject_id = ids.split(",")[0]
        class_id = ids.split(",")[1]
        teacher_id = ids.split(",")[2]
        sql = f"""SELECT
                    s.id,
                    s.first_name,
                    s.last_name,
                    s.student_id,
                    s.class_id,
                    c.class_name,
                    t.teacher_id,
                    t.teacher_name,
                    su.subject_id,
                    su.subject_name
                FROM
                    (SELECT
                        id,
                        first_name,
                        last_name,
                        student_id,
                        teacher_id,
                        class_id,
                        subject_id
                    FROM Student
                    where teacher_id = '{teacher_id}'
                    AND class_id = '{class_id}'
                    AND subject_id = '{subject_id}'
                    ) s
                LEFT JOIN
                    (SELECT
                        id,
                        name AS class_name
                    FROM class
                    where id = '{class_id}') c
                ON s.class_id = c.id
                LEFT JOIN
                    (SELECT
                        id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name,
                        teacher_id
                    FROM teacher
                    where id = '{teacher_id}') t
                ON s.teacher_id = t.id
                LEFT JOIN
                (SELECT
                    id as subject_id,
                    name as subject_name,
                    class_id
                FROM subject
                where id = '{subject_id}') su
                ON su.class_id = s.class_id"""

        students = self.con.select_all(sql)
        result = list()
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["first_name"] = student[1]
            data["last_name"] = student[2]
            data["student_id"] = student[3]
            data["class_id"] = student[4]
            data["class_name"] = student[5]
            data["teacher_id"] = student[6]
            data["teacher_name"] = student[7]
            data["subject_id"] = student[8]
            data["subject_name"] = student[9]
            result.append(data)
        return result

    def get_student(self, id):
        sql = f"""SELECT
                    s.id,
                    s.first_name,
                    s.last_name,
                    s.student_id,
                    s.class_id,
                    c.class_name,
                    s.teacher_id,
                    u.teacher_name,
                    u.teacher_id,
                    s.parent_id
                FROM
                    (SELECT
                        id,
                        first_name,
                        last_name,
                        student_id,
                        teacher_id,
                        parent_id,
                        class_id
                    FROM Student where id = '{id}') s
                LEFT JOIN
                    (SELECT
                        id,
                        name AS class_name
                    FROM class) c
                ON s.class_id = c.id
                LEFT JOIN
                    (SELECT
                        id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name,
                        teacher_id
                    FROM teacher) u
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
        data["teach_id"] = student[8]
        data["parent_id"] = student[9]
        return data

    def check_Student_exists(self, column: str, value) -> bool:
        sql = """SELECT count(*) FROM student WHERE {} ='{}' ;""".format(column, value)
        data = self.con.select_one(sql)
        if data[0] == 0:
            return False
        else:
            return True

    def check_student_subject_exists(
        self, column: str, value, column1: str, value1, column2: str, value2
    ) -> bool:
        sql = """SELECT count(*) FROM student_subjects WHERE {} ='{}' and {} = '{}' and {} = '{}' ;""".format(
            column, value, column1, value1, column2, value2
        )
        data = self.con.select_one(sql)
        if data is None or data[0] == 0:
            return False
        else:
            return True

    def add_student(self, **info) -> bool:
        try:
            data = dict()
            data["id"] = str(uuid4())
            data["student_id"] = info["id"]
            data["subject_id"] = info["subject_id"]
            self.con.insert_data("student_subjects", **data)
            if self.check_Student_exists("student_id", info["student_id"]):
                return False, "Student already exists Please enter a new Student Id"

            self.con.insert_data("student", **info)
            return True, "Data Inserted Successfully!"

        except:  # noqa: E722
            return False, "A system error occurred, please try again later"

    def add_student_to_subject(self, **info) -> bool:
        try:
            if self.check_student_subject_exists(
                "student_id",
                info["student_id"],
                "subject_id",
                info["subject_id"],
                "class_id",
                info["class_id"],
            ):
                return False, "Student already Added to this Subject"
            self.con.insert_data("student_subjects", **info)
            return True, "Data Inserted Successfully!"

        except:  # noqa: E722
            return False, "A system error occurred, please try again later"

    def update_student(self, **info) -> bool:
        try:
            if not self.check_Student_exists("student_id", info["student_id"]):
                return False, "Student Id not exist"
            Id = info["id"]
            del info["id"]
            self.con.update_data("student", Id, **info)

            return True, "Update Data Successfully!"
        except:  # noqa: E722
            return False, "A system error occurred, please try again later"

    def update_student_parent(self, **info) -> bool:
        try:
            if not self.check_Student_exists("id", info["id"]):
                return False, "Student Id not exist"
            Id = info["id"]
            del info["id"]
            self.con.update_data("student", Id, **info)

            return True, "Update Data Successfully!"
        except:  # noqa: E722
            return False, "A system error occurred, please try again later"

    def get_student_by_parent_id(self, id):
        sql = f"""SELECT
                    s.id,
                    s.first_name,
                    s.last_name,
                    s.student_id,
                    s.class_id,
                    c.class_name,
                    t.teacher_id,
                    t.teacher_name,
                    su.subject_id,
                    su.subject_name
                FROM
                    (SELECT
                        id,
                        first_name,
                        last_name,
                        student_id,
                        teacher_id,
                        class_id,
                        subject_id,
                        parent_id
                    FROM Student
                    WHERE parent_id = '{id}') s
                LEFT JOIN
                    (SELECT
                        id,
                        name AS class_name
                    FROM class) c
                ON s.class_id = c.id
                LEFT JOIN
                    (SELECT
                        id,
                        CONCAT(first_name, ' ', last_name) AS teacher_name,
                        teacher_id
                    FROM teacher) t
                ON s.teacher_id = t.id
                LEFT JOIN
                (SELECT
                    id as subject_id,
                    name as subject_name,
                    class_id
                FROM subject) su
                ON su.class_id = s.class_id

                LEFT JOIN
                (SELECT
                    id,
                    subject_id,
                    student_id,
                    class_id
                FROM student_subjects) ss
                ON s.id = ss.student_id
                AND su.subject_id = ss.subject_id
                AND c.id = ss.class_id
                """

        students = self.con.select_all(sql)
        result = list()
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["first_name"] = student[1]
            data["last_name"] = student[2]
            data["student_id"] = student[3]
            data["class_id"] = student[4]
            data["class_name"] = student[5]
            data["teacher_id"] = student[6]
            data["teacher_name"] = student[7]
            data["subject_id"] = student[8]
            data["subject_name"] = student[9]
            result.append(data)
        return result

    def calculate_gpa(self, class_id, student_id):
        sql = f"""SELECT
                    s.id,
                    s.participation,
                    s.home_work,
                    s.class_work,
                    s.quiz,
                    s.mid_term,
                    s.final,
                    t.term_id,
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
                    FROM marks
                    WHERE student_id = '{student_id}'
                    AND class_id ='{class_id}') s
                LEFT JOIN
                (SELECT
                        id,
                        term_id,
                        mark_id
                    FROM term_marks) mt
                ON s.id = mt.mark_id
                LEFT JOIN
                    (SELECT distinct
                        id as term_id,
                        name as term_name
                    FROM terms) t
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
                data["term_id"] = student[7]
                data["term_name"] = student[8]
                result.append(data)

        return result
