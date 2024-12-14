from src.models.subjects import SubjectModel


class Subject:
    def __init__(self):
        self.data = dict()
        self.data["title"] = "Subjects"
        self.subject = SubjectModel()

    def get_all_subjects_by_class_id(self, id):
        self.data["subjects"] = self.subject.get_all_subjects_by_class_id(id)

    def get_all_subjects_by_teacher_id(self, id):
        self.data["subjects"] = self.subject.get_all_subjects_by_teacher_id(id)

    def get_all_subjects(self):
        self.data["student_subjects"] = self.subject.get_all_subjects()

    def get_subject(self, id):
        self.data["subject"] = self.subject.get_subject(id)

    def add_subject(self, **info):
        return self.subject.add_subject(**info)

    def update_subject(self, **info):
        return self.subject.update_subject(**info)
