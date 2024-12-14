from src.models.classes import ClassModel


class Classes:
    def __init__(self):
        self.data = dict()
        self.data["title"] = "Classes"
        self.classes = ClassModel()

    def get_all_classes(self):
        self.data["classes"] = self.classes.get_all_classes()

    def get_class(self, id):
        self.data["class"] = self.classes.get_class(id)

    def get_class_details(self, id):
        self.data["class_details"] = self.classes.get_class_details(id)

    def add_class(self, **info):
        return self.classes.add_class(**info)

    def update_class(self, **info):
        return self.classes.update_class(**info)
