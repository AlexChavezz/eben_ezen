from werkzeug.security import check_password_hash
from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, user_id,  username, id_role, password) -> None:
        self.id = user_id
        self.username = username
        self.id_role = id_role
        self.password = password
    @classmethod
    def check_password(self, hased_password, password):
        return check_password_hash(hased_password, password)