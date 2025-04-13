import binascii
import hashlib
import os
import re

from src.database.database import DataBase


class TeacherModel:
    def __init__(self):
        self.con = DataBase()

    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
        pwdhash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode("ascii")

    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac(
            "sha512", provided_password.encode("utf-8"), salt.encode("ascii"), 100000
        )
        pwdhash = binascii.hexlify(pwdhash).decode("ascii")
        return pwdhash == stored_password

    def check_teacher_exists(self, column, value):
        sql = """SELECT count(*) FROM Teacher WHERE {} ='{}' ;""".format(column, value)
        data = self.con.select_one(sql)
        print(data)
        if data[0] == 0:
            return False
        else:
            return True

    def add_teacher(self, **info):
        try:
            """
            This function adds information to the database
            that the user entered in the fields in the (Sinup) interface :
            ( First Name , Last Name , Username , Email , Phone , Password ,Birthday,
              Gender  Country  )

            Initially it checks whether the entry is correct or incorrect and
            returns an error message in this case

            After , data is sent to the database to make sure the entered data
            is not duplicate

            If correct returns a message that the operation completed
            successfully and if there is an error returns an error message with
            the duplicate data specified
            """

            Email_Pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            email = info["email"]
            if not re.search(Email_Pattern, email):
                return False, "please enter a valid email address"

            if self.check_teacher_exists("email", email):
                return False, "An email already exists Please enter a new email"

            if self.check_teacher_exists("teacher_id", info["teacher_id"]):
                return False, "Teacher ID exists Please enter a new ID"

            info["password"] = self.hash_password(info["password"])

            self.con.insert_data("teacher", **info)
            # sql = "SELECT id FROM Teacher WHERE email='{}' ; ".format(info["email"])
            # Id_User = self.con.select_one(sql)
            return True, "Data Inserted Successfully!"
        except:  # noqa: E722
            return False, "System error occurred, please try again later"

    def Login_func(self, **info) -> int:
        """
        This function makes sure that the logon information is correct
        """
        try:
            sql = "SELECT id ,email , password, type  FROM user WHERE email='{}'  ;".format(
                info["email"].lower()
            )
            data = self.con.select_one(sql)
            if len(data) == 0:
                return False, "Email does not exist"
        except:  # noqa: E722
            return False, "Email does not exist"

        try:
            if self.verify_password(data[2], info["password"]):
                return True, data[0]
            else:
                return False, "Please enter a valid password"
        except:  # noqa: E722
            return False, "Please enter a valid password"

    def get_info_user_by_Id(self, Id_User: int):
        sql = f"""select id, first_name, last_name, email, type from user where id = '{Id_User}'  ; """

        User_info = self.con.select_one(sql)
        data = dict()
        data["id"] = User_info[0]
        data["first_name"] = User_info[1]
        data["last_name"] = User_info[2]
        data["email"] = User_info[3]
        data["type"] = User_info[4]
        return data

    def get_teacher(self, Id_User: int):
        sql = f"""select id, first_name, last_name, email, type FROM Teacher where id = '{Id_User}'  ; """

        User_info = self.con.select_one(sql)
        data = dict()
        data["id"] = User_info[0]
        data["first_name"] = User_info[1]
        data["last_name"] = User_info[2]
        data["email"] = User_info[3]
        data["type"] = User_info[4]
        return data

    def get_teacher_classes(self, id):
        sql = f"""SELECT id , class_id, name , tea_id, teacher_name
                FROM (
                    select id , concat(first_name, ' ',last_name) as teacher_name, teacher_id
                    from user
                ) u
                left join
                (
                    select id as class_id, name , teacher_id as tea_id
                    from Class
                ) c
                on u.teacher_id = c.tea_id
                where u.id = {id} """

        teacher_classes = self.con.select_all(sql)
        result = list()
        for teacher in teacher_classes:
            data = dict()
            data["id"] = teacher[0]
            data["class_id"] = teacher[1]
            data["name"] = teacher[2]
            data["teacher_id"] = teacher[3]
            data["teacher_name"] = teacher[4]
            result.append(data)
        return result

    def get_all_teachers(self):
        sql = """ select id , teacher_id, concat(first_name, ' ',last_name) as teacher_name
                    FROM Teacher """

        teacher_classes = self.con.select_all(sql)
        result = list()
        for teacher in teacher_classes:
            data = dict()
            data["id"] = teacher[0]
            data["teacher_id"] = teacher[1]
            data["teacher_name"] = teacher[2]
            result.append(data)
        return result
