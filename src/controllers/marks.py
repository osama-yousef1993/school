from src.models.marks import MarksModel
from src.models.terms import TermsModel


class Mark:
    def __init__(self):
        self.data = dict()
        self.data["title"] = "Marks"
        self.marks = MarksModel()
        self.terms = TermsModel()

    def get_student_marks(self, student_id, subject_id):
        self.data["terms"] = self.terms.get_all_terms()
        self.data["mark"] = self.marks.get_student_marks(student_id, subject_id)
        for term in self.data["terms"]:
            for mark in self.data["mark"]:
                if term["id"] == mark["term_id"]:
                    name = term["name"].split(" ")[0]
                    key = f"{name.lower()}_term"
                    self.data[key] = mark

    def add_mark(self, info):
        result = tuple()
        for data in info:
            status = self.marks.add_mark(**data)
            if status[0]:
                result = status
            else:
                result = status
        return result

    def update_mark(self, **info):
        return self.marks.update_mark(**info)
