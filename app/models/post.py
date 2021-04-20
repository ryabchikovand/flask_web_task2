"""
Модуль содержащий детальное описание
модели Post
"""

from app import db
from datetime import datetime
from flask_login import UserMixin


class Post(UserMixin, db.Model):
    """
    Модель поста
    согласно схеме содержит 4 атрибута:
    * id - идентификатор поста
    * body - тело поста
    * timestamp - время создания поста
    * user_id - идентификатор пользователя из таблицы users

    еще добавим 2 метода для отладки: __str__, __repr__
    """
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    body = db.Column(db.String(450))
    time_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    time_updated = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author = db.Column(db.String(200))
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __str__(self):
        return f"Post object (title:{self.title}, body:{self.body})"

    def __repr__(self):
        return f"<Post [title:{self.title}, body:{self.body}]>"