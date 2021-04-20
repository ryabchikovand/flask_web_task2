"""
Модуль, содержащий набор веб-форм
для взаимодействия пользователя с нашим приложением
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models.user import User


class EditForm(FlaskForm):
    """
    Класс, описывающий форму для изменения пароля для залогированного пользователя
    """
    old_password = PasswordField(label="Password", validators=[DataRequired()])
    new_password_1 = PasswordField(label="New Password", validators=[DataRequired()])
    new_password_2 = PasswordField(label="New Password (again)", validators=[DataRequired(), EqualTo('new_password_1')])
    submit = SubmitField(label="Confirm change password")

    user = None

    def set_current_user(self, current_user: User):
        self.user = current_user

    def validate_old_password(self, old_password):
        """
        Проверяет, совпадает ли старый пароль
        :param old_password:
        :return:
        """
        if not self.user.check_password(old_password.data):
            raise ValidationError('Enter correct password')

        if old_password.data == self.new_password_1.data or old_password.data == self.new_password_1.data:
            raise ValidationError('Error: New password match')


class LoginForm(FlaskForm):
    """
    Класс, описывающий форму для логина пользователя
    """
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember_me = BooleanField(label="Remember?")
    submit = SubmitField(label="Log In Button")


class RegisterForm(FlaskForm):
    """
    Класс, описывающий форму для регистрации пользователя
    """
    username = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    password2 = PasswordField(label="Password(again)", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label="Register")

    def validate_username(self, username):
        """
        Проверяет, есть ли в бд пользователь с таким username
        """
        user = User.query.filter_by(username=username.data).first() 
        if user is not None:
            raise ValidationError('This username already taken')

    def validate_email(self, email):
        """
        Проверяет, есть ли в бд пользователь с таким email
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use different email')


# 1. Сначала будут запущены ВСЕ валидаторы, которые определены в полях validators
# 2. Если стандартные валидаторы молчат (не бросают исключений), то управление передается методам, которые начинаются 
# со слова validate_
# 3. Если наши методы не выбрасывают исключений - значит форма валидна