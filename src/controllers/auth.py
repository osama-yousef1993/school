from src.models.auth import Register_And_login


class Users:
    def __init__(self):
        self.data = dict()
        self.data["title"] = "My Account"
        self.register_user = Register_And_login()

    def get_info_user_by_Id(self, Id_User):
        self.data["User"] = self.register_user.get_info_user_by_Id(Id_User)

    def login(self, **info):
        result = tuple()
        result = self.register_user.Login_func(**info)
        if not result[0]:
            result = self.register_user.teacher_Login_func(**info)
        return result

    def Add_User(self, **info):
        return self.register_user.Register_func(**info)

    def get_teacher_classes(self, id):
        self.data["classes"] = self.register_user.get_teacher_classes(id)

    def get_all_teachers(self):
        self.data["teachers"] = self.register_user.get_all_teachers()

    def get_all_parents(self):
        self.data["parents"] = self.register_user.get_all_parents()

    def update_user(self, **info):
        return self.register_user.update_user(**info)
