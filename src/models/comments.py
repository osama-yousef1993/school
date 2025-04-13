from src.database.database import DataBase


class CommentsModel:
    def __init__(self):
        self.con = DataBase()

    def get_comments_by_parent_id(self, ids):
        parent_id = ids.split(",")[0]
        teacher_id = ids.split(",")[1]
        subject_id = ids.split(",")[2]
        student_id = ids.split(",")[3]
        sql = f"""
        SELECT
            id,
            teacher_id,
            parent_id,
            student_id,
            subject_id,
            comments,
            date_added,
            from_who
            from Comments
            where parent_id = '{parent_id}'
            AND teacher_id = '{teacher_id}'
            AND subject_id = '{subject_id}'
            AND student_id = '{student_id}'
            order by date_added asc
        """

        students = self.con.select_all(sql)
        result = list()
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["teacher_id"] = student[1]
            data["parent_id"] = student[2]
            data["student_id"] = student[3]
            data["subject_id"] = student[4]
            data["comments"] = student[5]
            data["date_added"] = student[6]
            data["from_who"] = student[7]
            result.append(data)
        return result

    def get_comments_by_parent_teacher_id(self, ids):
        student_id = ids.split(",")[0]
        subject_id = ids.split(",")[1]
        teacher_id = ids.split(",")[2]
        parent_id = ids.split(",")[3]
        sql = f"""
        SELECT
            id,
            teacher_id,
            parent_id,
            student_id,
            subject_id,
            comments,
            date_added,
            from_who
            from Comments
            where parent_id = '{parent_id}'
            AND teacher_id = '{teacher_id}'
            AND subject_id = '{subject_id}'
            AND student_id = '{student_id}'
            order by date_added asc
        """

        students = self.con.select_all(sql)
        result = list()
        for student in students:
            data = dict()
            data["id"] = student[0]
            data["teacher_id"] = student[1]
            data["parent_id"] = student[2]
            data["student_id"] = student[3]
            data["subject_id"] = student[4]
            data["comments"] = student[5]
            data["date_added"] = student[6]
            data["from_who"] = student[7]
            result.append(data)
        return result

    def add_comments(self, **info) -> bool:
        try:
            self.con.insert_data("comments", **info)
            return True, "Data Inserted Successfully!"

        except Exception as e:  # noqa: E722
            print(e)
            return False, "A system error occurred, please try again later"
