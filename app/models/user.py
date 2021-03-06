"""
Модуль содержащий подробное описание модели User
"""
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    """
    Модель пользователя
    согласно схеме содержит 4 атрибута:
    * id 
    * username  - уникальный
    * password_hash - закодированный пароль пользователя
    * email - уникальный

    еще добавим 2 метода для отладки: __str__, __repr__
    2 метода для работы с паролем:
        * set_password(pure_pass) - > hash_pass
        * chechk_password(semi_pure_pass) -> bool
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(64), index=True, unique=True) 
    password_hash = db.Column(db.String(128)) 
    email = db.Column(db.String(120), index=True, unique=True) 
    # posts = db.relationship("Post", backref="author", lazy="dynamic")

    def set_password(self, pure_pass:str):
        """
        Устанавливает значение атрибуту password_hash
        при регистрации (чаще всего)
        """
        self.password_hash = generate_password_hash(pure_pass)

    def check_password(self, semi_pure_pass:str) -> bool:
        """
        Возвращает True если password_hash был сегенерирован на основе 
        semi_pure_pass, и False в противном случае
        """
        return check_password_hash(self.password_hash, semi_pure_pass)


    def __str__(self):
        return f"User object (username:{self.username}, email:{self.email})"

    def __repr__(self):
        return f"<User [username:{self.username}, email:{self.email}]>"


@login.user_loader
def load_user(id:int) -> User:
    """
    Находит юзера в бд по ID
    """
    return User.query.get(int(id))