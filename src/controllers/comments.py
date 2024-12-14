from src.models.comments import CommentsModel


class Comments:
    def __init__(self):
        self.data = dict()
        self.data["title"] = "Comments"
        self.comments = CommentsModel()

    def get_comments_by_parent_id(self, ids):
        self.data["comments"] = self.comments.get_comments_by_parent_id(ids)

    def get_comments_by_parent_teacher_id(self, ids):
        self.data["parent_comments"] = self.comments.get_comments_by_parent_teacher_id(ids)

    def add_comments(self, **info):
        return self.comments.add_comments(**info)
