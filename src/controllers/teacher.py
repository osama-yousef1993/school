from src.models.teacher import TeacherModel


class Teacher:
    def __init__(self):
        self.data = dict()
        self.data["title"] = "Teachers"
        self.teacher = TeacherModel()

    def get_all_teachers(self):
        self.data["teachers"] = self.teacher.get_all_teachers()

    def add_teacher(self, **info):
        return self.teacher.add_teacher(**info)

    def get_teacher(self, id):
        self.data["teacher"] = self.teacher.get_teacher(id)
