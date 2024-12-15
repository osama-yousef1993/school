from src.models.students import StudentModel


class Student:
    def __init__(self):
        self.data = dict()
        self.data["title"] = "Student"
        self.student = StudentModel()

    def get_all_students(self):
        self.data["students"] = self.student.get_all_students()

    def get_all_students_by_class_id(self, id):
        self.data["students_class"] = self.student.get_all_students_by_class_id(id)

    def get_all_students_by_subject_id(self, id):
        self.data["students_subject"] = self.student.get_all_students_by_subject_id(id)

    def get_all_students_by_teacher_id(self, ids):
        self.data["students_teacher"] = self.student.get_all_students_by_teacher_id(ids)

    def get_student_by_parent_id(self, id):
        self.data["student_parent"] = self.student.get_student_by_parent_id(id)

    def get_student(self, id):
        self.data["student"] = self.student.get_student(id)

    def add_student(self, **info):
        return self.student.add_student(**info)

    def add_student_to_subject(self, **info):
        return self.student.add_student_to_subject(**info)

    def update_student(self, **info):
        return self.student.update_student(**info)

    def update_student_parent(self, **info):
        return self.student.update_student_parent(**info)

    def calculate_gpa(self, class_id, student_id):
        self.data["gpas"] = self.student.calculate_gpa(class_id, student_id)
        self.calculate_student_gpa()

    def calculate_student_gpa(self):
        data = self.data["gpas"]
        first_term = 0.0
        second_term = 0.0
        first_term_count = 0
        second_term_count = 0
        for gpa in data:
            if gpa["term_name"] == "First Term":
                first_term += (
                    gpa["participation"]
                    + gpa["home_work"]
                    + gpa["class_work"]
                    + gpa["quiz"]
                    + gpa["mid_term"]
                    + gpa["final"]
                ) * 3
                first_term_count += 3
            elif gpa["term_name"] == "Second Term":
                second_term += (
                    gpa["participation"]
                    + gpa["home_work"]
                    + gpa["class_work"]
                    + gpa["quiz"]
                    + gpa["mid_term"]
                    + gpa["final"]
                ) * 3
                second_term_count += 3
        self.data["first_term_gpa"] = first_term / first_term_count
        self.data["second_term_gpa"] = second_term / second_term_count
        self.data["total_gpa"] = (first_term + second_term) / (
            first_term_count + second_term_count
        )
