from datetime import datetime
from uuid import uuid4

from flask import Flask, redirect, render_template, request, session, url_for

from src.controllers.auth import Users
from src.controllers.classes import Classes
from src.controllers.comments import Comments
from src.controllers.marks import Mark
from src.controllers.students import Student
from src.controllers.subjects import Subject
from src.controllers.teacher import Teacher
from src.controllers.terms import Term
from src.utils.config import DEBUG, HOST_APP, PORT

app = Flask(__name__)

app.secret_key = "abcdefghijklmn"


# done
@app.route("/")
def index():
    return redirect(url_for("home_page"))


# done
@app.route("/home")
def home_page():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    if user_data.data["User"]["type"] == "Admin":
        classes_result = Classes()
        classes_result.get_all_classes()
        classes_result.data["User"] = user_data.data["User"]
        return render_template("classes.html", data=classes_result.data)
    elif user_data.data["User"]["type"] == "teacher":
        return redirect(
            url_for("subjects_teacher_table_page", teacher_id=session["Id_User"])
        )
    elif user_data.data["User"]["type"] == "parent":
        return redirect(url_for("student_parent_table", parent_id=session["Id_User"]))


# done
@app.route("/classes-table")
def classes_table_page():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    classes_result = Classes()
    classes_result.get_all_classes()
    classes_result.data["User"] = user_data.data["User"]
    if "add_class_error" in session:
        classes_result.data["Messages_Error"] = session["add_class_error"]
        del session["add_class_error"]
    elif "successfully_add_class" in session:
        classes_result.data["Messages_Successfully"] = session["successfully_add_class"]
        del session["successfully_add_class"]
    return render_template("tables/classes.html", data=classes_result.data)


# done
@app.route("/classes-form")
def classes_form_page():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    return render_template("forms/classes.html", data=user_data.data)


# done
@app.route("/add_class", methods=["POST"])
def add_class():
    data = dict()
    classes_res = Classes()
    if request.method == "POST":
        data["id"] = str(uuid4())
        data["name"] = request.form["name"]
        status = classes_res.add_class(**data)
        if status[0]:
            session["successfully_add_class"] = status[1]
            return redirect(url_for("classes_table_page"))
        elif not status[0]:
            session["add_class_error"] = status[1]
            return redirect(url_for("classes_table_page"))
    else:
        return redirect(url_for("classes_form_page"))


# # done
@app.route("/student_parent_table/<parent_id>")
def student_parent_table(parent_id):
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    student_data = Student()
    student_data.get_student_by_parent_id(parent_id)
    class_res = Classes()
    class_res.get_all_classes()
    if user_data.data["User"]["type"] == "Admin":
        if len(student_data.data["student_parent"]) == 0:
            session["student_error"] = "there is no Child for this Parent"
            return redirect(url_for("parents_table_page"))
        student_data.data["User"] = user_data.data["User"]
        student_data.data["classes"] = class_res.data["classes"]
        return render_template("tables/student_parent.html", data=student_data.data)
    elif user_data.data["User"]["type"] == "parent":
        student_data.data["User"] = user_data.data["User"]
        student_data.data["classes"] = class_res.data["classes"]
        return render_template("tables/student_parent.html", data=student_data.data)


# done
@app.route("/subjects-table/<class_id>")
def subjects_table_page(class_id):
    if "Id_User" not in session:
        return redirect(url_for("login"))
    subject_class = Subject()
    subject_class.get_all_subjects_by_class_id(class_id)
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    subject_class.data["User"] = user_data.data["User"]
    subject_class.data["User"]["class_id"] = class_id
    if "add_subject_error" in session:
        subject_class.data["Messages_Error"] = session["add_subject_error"]
        del session["add_subject_error"]
    elif "successfully_add_subject" in session:
        subject_class.data["Messages_Successfully"] = session[
            "successfully_add_subject"
        ]
        del session["successfully_add_subject"]
    return render_template("tables/subjects.html", data=subject_class.data)


# done
@app.route("/subjects-form/<class_id>")
def subjects_form_page(class_id):
    if "Id_User" not in session:
        return redirect(url_for("login"))
    teacher_class = Teacher()
    teacher_class.get_all_teachers()
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    teacher_class.data["User"] = user_data.data["User"]
    teacher_class.data["User"]["class_id"] = class_id
    return render_template("forms/subjects.html", data=teacher_class.data)


# done
@app.route("/add_subject", methods=["POST"])
def add_subject():
    data = dict()
    subject_res = Subject()
    if request.method == "POST":
        data["id"] = str(uuid4())
        data["name"] = request.form["name"]
        data["class_id"] = request.form["class_id"]
        data["teacher_id"] = request.form["teacher"]
        status = subject_res.add_subject(**data)
        if status[0]:
            session["successfully_add_subject"] = status[1]
            return redirect(url_for("subjects_table_page", class_id=data["class_id"]))
        elif not status[0]:
            session["add_subject_error"] = status[1]
            return redirect(url_for("subjects_table_page", class_id=data["class_id"]))
    else:
        return redirect(url_for("subjects_form_page", class_id=data["class_id"]))


# done
@app.route("/teachers-table")
def teachers_table_page():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    teacher_class = Teacher()
    teacher_class.get_all_teachers()
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    teacher_class.data["User"] = user_data.data["User"]
    if "add_teacher_error" in session:
        teacher_class.data["Messages_Error"] = session["add_teacher_error"]
        del session["add_teacher_error"]
    elif "successfully_add_teacher" in session:
        teacher_class.data["Messages_Successfully"] = session[
            "successfully_add_teacher"
        ]
        del session["successfully_add_teacher"]
    return render_template("tables/teacher.html", data=teacher_class.data)


# done
@app.route("/teacher-form")
def teachers_form_page():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    return render_template("forms/teacher.html", data=user_data.data)


# done
@app.route("/add_teacher", methods=["POST"])
def add_teacher():
    data = dict()
    teacher_res = Teacher()
    if request.method == "POST":
        data["id"] = str(uuid4())
        data["first_name"] = request.form["first_name"]
        data["last_name"] = request.form["last_name"]
        data["email"] = request.form["email"]
        data["password"] = request.form["pass"]
        data["teacher_id"] = request.form["teacher_id"]
        data["type"] = "teacher"
        status = teacher_res.add_teacher(**data)
        if status[0]:
            session["successfully_add_teacher"] = status[1]
            return redirect(url_for("teachers_table_page"))
        elif not status[0]:
            session["add_teacher_error"] = status[1]
            return redirect(url_for("teachers_table_page"))
    else:
        return redirect(url_for("teachers_form_page"))


# done
@app.route("/students-subject-table/<subject_id>")
def students_subject_table_page(subject_id):
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    student_class = Student()
    student_class.get_all_students_by_subject_id(subject_id)
    user_data.get_info_user_by_Id(session["Id_User"])
    student_class.data["User"] = user_data.data["User"]
    return render_template(
        "tables/students_subject_table.html", data=student_class.data
    )


# done
@app.route("/students-table")
def students_table_page():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    student_class = Student()
    student_class.get_all_students()
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    student_class.data["User"] = user_data.data["User"]
    if "add_student_error" in session:
        student_class.data["Messages_Error"] = session["add_student_error"]
        del session["add_student_error"]
    elif "successfully_add_student" in session:
        student_class.data["Messages_Successfully"] = session[
            "successfully_add_student"
        ]
        del session["successfully_add_student"]
    return render_template("tables/students.html", data=student_class.data)


# done
@app.route("/student-form")
def student_form_page():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    classes_res = Classes()
    classes_res.get_all_classes()
    teacher_class = Teacher()
    teacher_class.get_all_teachers()
    subject_class = Subject()
    subject_class.get_all_subjects()
    student_class = Student()
    student_class.get_all_students()
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    teacher_class.data["User"] = user_data.data["User"]
    teacher_class.data["subjects"] = subject_class.data["student_subjects"]
    teacher_class.data["classes"] = classes_res.data["classes"]
    teacher_class.data["students"] = student_class.data["students"]
    return render_template("forms/students.html", data=teacher_class.data)


# done
@app.route("/add_student", methods=["POST"])
def add_student():
    data = dict()
    student_res = Student()
    if request.method == "POST":
        data["id"] = str(uuid4())
        data["first_name"] = request.form["first_name"]
        data["last_name"] = request.form["last_name"]
        data["student_id"] = request.form["student_id"]
        data["class_id"] = request.form["class"]
        data["teacher_id"] = request.form["teacher"]
        res = request.form["subject"].split(",")
        data["subject_id"] = res[0]
        status = student_res.add_student(**data)
        if status[0]:
            session["successfully_add_student"] = status[1]
            return redirect(url_for("students_table_page"))
        elif not status[0]:
            session["add_student_error"] = status[1]
            return redirect(url_for("students_table_page"))
    else:
        return redirect(url_for("student_form_page"))


@app.route("/calculate_gpa", methods=["POST"])
def calculate_gpa():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    data = dict()
    if request.method == "POST":
        data["class_id"] = request.form["class"]
        data["student_id"] = request.form["student"]
        ids = ",".join([data["class_id"], data["student_id"]])
        return redirect(url_for("gpa", ids=ids))
    else:
        return redirect(url_for("student_parent_table", parent_id=session["Id_User"]))


@app.route("/gpa/<ids>")
def gpa(ids):
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    class_id = ids.split(",")[0]
    student_id = ids.split(",")[1]
    student_class = Student()
    student_class.calculate_gpa(class_id, student_id)
    user_data.data["first_term_gpa"] = student_class.data["first_term_gpa"]
    user_data.data["second_term_gpa"] = student_class.data["second_term_gpa"]
    user_data.data["total_gpa"] = student_class.data["total_gpa"]
    return render_template("tables/gpa_table.html", data=user_data.data)


@app.route("/add_student_subject", methods=["POST"])
def add_student_subject():
    data = dict()
    student_res = Student()
    if request.method == "POST":
        data["id"] = str(uuid4())
        data["subject_id"] = request.form["subject"].split(",")[0]
        data["student_id"] = request.form["student"]
        data["class_id"] = request.form["class"]
        status = student_res.add_student_to_subject(**data)
        if status[0]:
            session["successfully_add_student"] = status[1]
            return redirect(url_for("students_table_page"))
        elif not status[0]:
            session["add_student_error"] = status[1]
            return redirect(url_for("students_table_page"))
    else:
        return redirect(url_for("student_form_page"))


# done
@app.route("/mark-student-form/<ids>")
def mark_student_form_page(ids):
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    student_id = ids.split(",")[0]
    subject_id = ids.split(",")[1]
    student_class = Student()
    subject_class = Subject()
    mark_class = Mark()
    term_class = Term()
    student_class.get_student(student_id)
    subject_class.get_subject(subject_id)
    mark_class.get_student_marks(student_id, subject_id)
    term_class.get_all_terms()
    subject_class.data["student"] = student_class.data["student"]
    subject_class.data["User"] = user_data.data["User"]
    subject_class.data["mark"] = mark_class.data["mark"]
    subject_class.data["terms"] = term_class.data["terms"]
    if "first_term" in mark_class.data.keys():
        subject_class.data["first_term"] = mark_class.data["first_term"]
    else:
        subject_class.data["first_term"] = dict()
    if "second_term" in mark_class.data.keys():
        subject_class.data["second_term"] = mark_class.data["second_term"]
    else:
        subject_class.data["second_term"] = dict()
    return render_template("forms/mark-student-form.html", data=subject_class.data)


# done
@app.route("/mark-student-table/<ids>")
def mark_student_table_page(ids):
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    student_id = ids.split(",")[0]
    subject_id = ids.split(",")[1]
    student_class = Student()
    subject_class = Subject()
    mark_class = Mark()
    term_class = Term()
    comment_class = Comments()
    mark_class.get_student_marks(student_id, subject_id)
    student_class.get_student(student_id)
    subject_class.get_subject(subject_id)
    term_class.get_all_terms()
    if all(
        i is not None or i != ""
        for i in [
            student_id,
            subject_id,
            session["Id_User"],
            student_class.data["student"]["parent_id"],
        ]
    ):
        ids = ",".join(
            [
                student_id,
                subject_id,
                session["Id_User"],
                student_class.data["student"]["parent_id"],
            ]
        )
        comment_class.get_comments_by_parent_teacher_id(ids)
        subject_class.data["parent_comments"] = comment_class.data["parent_comments"]
        subject_class.data["comments_data"] = {
            "student_id": student_id,
            "teacher_id": session["Id_User"],
            "subject_id": subject_id,
            "parent_id": student_class.data["student"]["parent_id"],
        }
    else:
        subject_class.data["parent_comments"] = dict()
    subject_class.data["student"] = student_class.data["student"]
    subject_class.data["User"] = user_data.data["User"]
    if "first_term" in mark_class.data.keys():
        subject_class.data["first_term"] = mark_class.data["first_term"]
    if "second_term" in mark_class.data.keys():
        subject_class.data["second_term"] = mark_class.data["second_term"]
    subject_class.data["mark"] = mark_class.data["mark"]
    subject_class.data["terms"] = term_class.data["terms"]
    if "add_mark_error" in session:
        subject_class.data["Messages_Error"] = session["add_mark_error"]
        del session["add_mark_error"]
    elif "successfully_add_mark" in session:
        subject_class.data["Messages_Successfully"] = session["successfully_add_mark"]
        del session["successfully_add_mark"]
    return render_template("tables/mark-student-table.html", data=subject_class.data)


# done
@app.route("/add_marks", methods=["POST"])
def add_mark():
    mark_res = Mark()
    inserted_data = list()
    if request.method == "POST":
        type = request.form["term_type"]
        type_second_term = request.form["term_type_second_term"]
        if type == "first":
            data = dict()
            data["id"] = (
                str(uuid4()) if request.form["id"] == "" else request.form["id"]
            )
            data["participation"] = (
                float(request.form["participation"])
                if request.form["participation"] != ""
                else 0
            )
            data["home_work"] = (
                float(request.form["home_work"])
                if request.form["home_work"] != ""
                else 0
            )
            data["class_work"] = (
                float(request.form["class_work"])
                if request.form["class_work"] != ""
                else 0
            )
            data["quiz"] = (
                float(request.form["quiz"]) if request.form["quiz"] != "" else 0
            )
            data["mid_term"] = (
                float(request.form["mid_term"]) if request.form["mid_term"] != "" else 0
            )
            data["final"] = (
                float(request.form["final"]) if request.form["final"] != "" else 0
            )
            data["student_id"] = request.form["student_id"]
            data["class_id"] = request.form["class_id"]
            data["subject_id"] = request.form["subject_id"]
            data["teacher_id"] = request.form["teacher_id"]
            data["terms_id"] = request.form["term_id"]
            data["mark_term_id"] = request.form["mark_term_id"]
            if any(
                [
                    data["participation"] != 0,
                    data["home_work"] != 0,
                    data["class_work"] != 0,
                    data["quiz"] != 0,
                    data["mid_term"] != 0,
                    data["final"] != 0,
                ]
            ):
                inserted_data.append(data)
        if type_second_term == "second":
            data = dict()
            data["id"] = (
                str(uuid4())
                if request.form["id_second_term"] == ""
                else request.form["id_second_term"]
            )
            data["participation"] = (
                float(request.form["participation_second_term"])
                if request.form["participation_second_term"] != ""
                else 0
            )
            data["home_work"] = (
                float(request.form["home_work_second_term"])
                if request.form["home_work_second_term"] != ""
                else 0
            )
            data["class_work"] = (
                float(request.form["class_work_second_term"])
                if request.form["class_work_second_term"] != ""
                else 0
            )
            data["quiz"] = (
                float(request.form["quiz_second_term"])
                if request.form["quiz_second_term"] != ""
                else 0
            )
            data["mid_term"] = (
                float(request.form["mid_term_second_term"])
                if request.form["mid_term_second_term"] != ""
                else 0
            )
            data["final"] = (
                float(request.form["final_second_term"])
                if request.form["final_second_term"] != ""
                else 0
            )
            data["student_id"] = request.form["student_id"]
            data["class_id"] = request.form["class_id"]
            data["subject_id"] = request.form["subject_id"]
            data["teacher_id"] = request.form["teacher_id"]
            data["terms_id"] = request.form["term_id_second_term"]
            data["mark_term_id"] = request.form["mark_term_id_second_term"]
            if any(
                [
                    data["participation"] != 0,
                    data["home_work"] != 0,
                    data["class_work"] != 0,
                    data["quiz"] != 0,
                    data["mid_term"] != 0,
                    data["final"] != 0,
                ]
            ):
                inserted_data.append(data)
        status = mark_res.add_mark(inserted_data)
        ids = f'{data["student_id"]},{data["subject_id"]}'
        if status[0]:
            session["successfully_add_mark"] = status[1]
            return redirect(url_for("mark_student_table_page", ids=ids))
        elif not status[0]:
            session["add_mark_error"] = status[1]
            return redirect(url_for("mark_student_table_page", ids=ids))
    else:
        return redirect(url_for("mark_student_form_page", ids=ids))


# done
@app.route("/marks-table/<id>")
def marks_table_page(id):
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    marks_class = Mark()
    ids = id.split(",")
    student_id = ids[0]
    subject_id = ids[1]
    marks_class.get_all_student_marks(student_id, subject_id)
    marks_class.data["User"] = user_data.data["User"]
    if "add_mark_error" in session:
        marks_class.data["Messages_Error"] = session["add_mark_error"]
        del session["add_mark_error"]
    elif "successfully_add_mark" in session:
        marks_class.data["Messages_Successfully"] = session["successfully_add_mark"]
        del session["successfully_add_mark"]
    return render_template("tables/marks.html", data=marks_class.data)


# done
@app.route("/marks-form")
def marks_form_page():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    teacher_class = Users()
    student_class = Student()
    teacher_class.get_all_teachers()
    student_class.get_all_students()
    teacher_class.data["students"] = student_class.data["students"]
    return render_template("forms/marks.html", data=teacher_class.data)


@app.route("/student/<student_id>")
def student_page(student_id):
    if "Id_User" not in session:
        return redirect(url_for("login"))
    student_class = Student()
    student_class.get_student(student_id)
    return render_template("students.html", data=student_class.data)


# done
@app.route("/student-parent-table/")
def student_parent_table_page():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    student_class = Student()
    student_class.get_student_by_parent_id(session["Id_User"])
    student_class.data["User"] = user_data.data["User"]
    return render_template("tables/student_parent_table.html", data=student_class.data)


#
#
#
#
# LogIn
#
#
#
# done
@app.route("/login")
def login():
    if "Id_User" in session:
        return redirect(url_for("home_page"))
    else:
        Users_Class = Users()
        if "Login_Error" in session:
            Users_Class.data["Login_Error"] = session["Login_Error"]
            del session["Login_Error"]
        return render_template("login.html", data=Users_Class.data)


# done
@app.route("/logout")
def Logout_Page():
    if "Id_User" in session:
        del session["Id_User"]
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


# done
@app.route("/login_check", methods=["POST"])
def check_Login_Page():
    data = dict()
    Users_Class = Users()
    if request.method == "POST":
        data["password"] = request.form["pass"]
        data["email"] = request.form["email"]

        # Check User Information
        status = Users_Class.login(**data)
        if status[0]:
            session["Id_User"] = status[1]
            return redirect(url_for("home_page"))
        elif not status[0]:
            session["Login_Error"] = status[1]
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


# done
@app.route("/register")
def register():
    Users_Class = Users()
    if "add_user_error" in session:
        Users_Class.data["Messages_Error"] = session["add_user_error"]
        del session["add_user_error"]
    elif "successfully_add_user" in session:
        Users_Class.data["Messages_Successfully"] = session["successfully_add_user"]
        del session["successfully_add_user"]
        return render_template(url_for("login"))

    return render_template("register.html", data=Users_Class.data)


# done
@app.route("/sign_up", methods=["POST"])
def sign_up_data():
    data = dict()
    Users_Class = Users()
    if request.method == "POST":
        data["id"] = str(uuid4())
        data["first_name"] = request.form["first_name"]
        data["last_name"] = request.form["last_name"]
        data["email"] = request.form["email"]
        data["password"] = request.form["pass"]
        data["type"] = "Admin"
        # Insert Data
        response = Users_Class.Add_User(**data)

        if response[0]:
            session["successfully_add_user"] = response[2]
            return redirect(url_for("login"))
        elif not response[0]:
            session["add_user_error"] = response[1]
            return redirect(url_for("register"))


# done
@app.route("/profile")
def profile():
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    if "update_user_error" in session:
        user_data.data["Messages_Error"] = session["update_user_error"]
        del session["update_user_error"]
    elif "successfully_update_user" in session:
        user_data.data["Messages_Successfully"] = session["successfully_update_user"]
        del session["successfully_update_user"]
    return render_template("details/user-profile.html", data=user_data.data)


# done
@app.route("/update-user-form")
def update_user_form():
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    return render_template("details/user-profile-form.html", data=user_data.data)


@app.route("/update-user", methods=["POST"])
def update_user_data():
    data = dict()
    Users_Class = Users()
    if request.method == "POST":
        data["id"] = request.form["id"]
        data["first_name"] = request.form["first_name"]
        data["last_name"] = request.form["last_name"]
        data["type"] = request.form["type"]
        # Insert Data
        response = Users_Class.update_user(**data)

        if response[0]:
            session["successfully_update_user"] = response[1]
            return redirect(url_for("profile"))
        elif not response[0]:
            session["update_user_error"] = response[1]
            return redirect(url_for("profile"))


# done
@app.route("/parents-table")
def parents_table_page():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_all_parents()
    user_data.get_info_user_by_Id(session["Id_User"])
    if "add_parent_error" in session:
        user_data.data["Messages_Error"] = session["add_parent_error"]
        del session["add_parent_error"]
    elif "student_error" in session:
        user_data.data["Messages_Error"] = session["student_error"]
        del session["student_error"]
    elif "successfully_add_parent" in session:
        user_data.data["Messages_Successfully"] = session["successfully_add_parent"]
        del session["successfully_add_parent"]
    elif "successfully_add_parent_to_student" in session:
        user_data.data["Messages_Successfully"] = session[
            "successfully_add_parent_to_student"
        ]
        del session["successfully_add_parent_to_student"]
    elif "add_parent_to_student_error" in session:
        user_data.data["Messages_Successfully"] = session["add_parent_to_student_error"]
        del session["add_parent_to_student_error"]
    return render_template("tables/parent.html", data=user_data.data)


# done
@app.route("/parent-form")
def parent_form_page():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    return render_template("forms/parent.html", data=user_data.data)


# done
@app.route("/add_parent", methods=["POST"])
def add_parent():
    data = dict()
    parent_res = Users()
    if request.method == "POST":
        data["id"] = str(uuid4())
        data["first_name"] = request.form["first_name"]
        data["last_name"] = request.form["last_name"]
        data["email"] = request.form["email"]
        data["password"] = request.form["pass"]
        data["type"] = "parent"
        status = parent_res.Add_User(**data)
        if status[0]:
            session["successfully_add_parent"] = status[2]
            return redirect(url_for("parents_table_page"))
        elif not status[0]:
            session["add_parent_error"] = status[1]
            return redirect(url_for("parents_table_page"))
    else:
        return redirect(url_for("parent_form_page"))


# done
@app.route("/student-parent-form")
def student_parent_form_page():
    if "Id_User" not in session:
        return redirect(url_for("login"))
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    user_data.get_all_parents()
    student_data = Student()
    student_data.get_all_students()
    user_data.data["students"] = student_data.data["students"]
    return render_template("forms/student-parent.html", data=user_data.data)


@app.route("/add_student_parent", methods=["POST"])
def add_student_parent():
    data = dict()
    student_res = Student()
    if request.method == "POST":
        data["id"] = request.form["student"]
        data["parent_id"] = request.form["parent"]
        status = student_res.update_student_parent(**data)
        if status[0]:
            session["successfully_add_parent_to_student"] = status[1]
            return redirect(url_for("parents_table_page"))
        elif not status[0]:
            session["add_parent_to_student_error"] = status[1]
            return redirect(url_for("parents_table_page"))
    else:
        return redirect(url_for("student_parent_form_page"))


# done
@app.route("/comments-form/<ids>")
def comments_form_page(ids):
    if "Id_User" not in session:
        return redirect(url_for("login"))
    comments_class = Comments()
    # parent_id = ids.split(",")[0]
    teacher_id = ids.split(",")[1]
    subject_id = ids.split(",")[2]
    student_id = ids.split(",")[3]
    comments_class.get_comments_by_parent_id(ids)
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    comments_class.data["User"] = user_data.data["User"]
    comments_class.data["comments_data"] = {
        "student_id": student_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
    }
    return render_template("forms/comments.html", data=comments_class.data)


# done
@app.route("/add_comments", methods=["POST"])
def add_comments():
    data = dict()
    comments_res = Comments()
    if request.method == "POST":
        data["id"] = str(uuid4())
        data["parent_id"] = request.form["parent_id"]
        data["teacher_id"] = request.form["teacher_id"]
        data["student_id"] = request.form["student_id"]
        data["subject_id"] = request.form["subject_id"]
        data["date_added"] = datetime.utcnow()
        data["comments"] = request.form["comments"]
        page_name = request.form["page_name"]
        if page_name == "student_mark":
            data["from_who"] = "teacher"
        elif page_name == "parent_mark":
            data["from_who"] = "parent"
        status = comments_res.add_comments(**data)
        ids = ",".join(
            [
                data["parent_id"],
                data["teacher_id"],
                data["subject_id"],
                data["student_id"],
            ]
        )
        if status[0]:
            if page_name != "student_mark":
                session["successfully_add_parent"] = status[1]
                return redirect(url_for("comments_form_page", ids=ids))
            else:
                ids = ",".join([data["student_id"], data["subject_id"]])
                return redirect(url_for("mark_student_table_page", ids=ids))

        elif not status[0]:
            if page_name != "student_mark":
                session["add_parent_error"] = status[1]
                return redirect(url_for("comments_form_page", ids=ids))
            else:
                ids = ",".join([data["student_id"], data["subject_id"]])
                return redirect(url_for("mark_student_table_page", ids=ids))
    else:
        return redirect(url_for("comments_form_page", ids=ids))


@app.route("/subjects-teacher-table/<teacher_id>")
def subjects_teacher_table_page(teacher_id):
    if "Id_User" not in session:
        return redirect(url_for("login"))
    subject_class = Subject()
    subject_class.get_all_subjects_by_teacher_id(teacher_id)
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    subject_class.data["User"] = user_data.data["User"]
    subject_class.data["User"]["class_id"] = teacher_id
    return render_template("tables/subjects-teacher.html", data=subject_class.data)


@app.route("/student-teacher-table/<ids>")
def student_teacher_table_page(ids):
    if "Id_User" not in session:
        return redirect(url_for("login"))
    student_class = Student()
    student_class.get_all_students_by_teacher_id(ids)
    user_data = Users()
    user_data.get_info_user_by_Id(session["Id_User"])
    student_class.data["User"] = user_data.data["User"]
    return render_template("tables/students-teacher.html", data=student_class.data)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT, host=HOST_APP)
