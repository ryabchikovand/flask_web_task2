"""
Модуль, содержащий набор веб-форм
для взаимодействия пользователя с нашим постами
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models.user import User
from app.models.post import Post


class CreatePostForm(FlaskForm):
    """
    Класс, описывающий форму для создания нового поста
    """
    title = StringField(label="Title", validators=[DataRequired()])
    body = TextAreaField(label="Body", validators=[DataRequired()])
    author = StringField(label="Author", validators=[DataRequired()])
    submit = SubmitField(label="Create")


class EditPostForm(FlaskForm):
    """
    Класс, описывающий форму для создания нового поста
    """
    title = StringField(label="Title")
    body = TextAreaField(label="Body")
    author = StringField(label="Author")
    submit = SubmitField(label="Update this Post")


class DeletePostForm(FlaskForm):
    """
    Класс, описывающий форму для удаления поста
    """
    submit = SubmitField(label="Delete this post")