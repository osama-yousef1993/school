from src.models.terms import TermsModel


class Term:
    def __init__(self):
        self.data = dict()
        self.data["title"] = "Terms"
        self.marks = TermsModel()

    def get_all_terms(self):
        self.data["terms"] = self.marks.get_all_terms()
