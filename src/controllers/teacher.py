from src.models.teacher import TeacherModel


class Teacher:
    def __init__(self):
        self.data = dict()
        self.data["title"] = "Teachers"
        self.teacher = TeacherModel()

    # def login(self, **info):
    #     return self.register_user.Login_func(**info)

    def add_teacher(self, **info):
        return self.teacher.add_teacher(**info)

    # def get_info_user_by_Id(self, Id_User):
    #     self.data["User"] = self.register_user.get_info_user_by_Id(Id_User)

    # def get_teacher_classes(self, id):
    #     self.data["classes"] = self.register_user.get_teacher_classes(id)

    def get_teacher(self, id):
        self.data["teacher"] = self.teacher.get_teacher(id)

    def get_all_teachers(self):
        self.data["teachers"] = self.teacher.get_all_teachers()
