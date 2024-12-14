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

    def update_student(self, **info):
        return self.student.update_student(**info)

    def update_student_parent(self, **info):
        return self.student.update_student_parent(**info)
