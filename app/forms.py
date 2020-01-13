# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    """
    Форма для авторизации пользователей сайта
    """
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class Like(FlaskForm):
    """
    Форма для сбора предпочтений пользователей
    """
    submit = SubmitField('Да!')


class RegistrationForm(FlaskForm):
    """
    Форма регистрации на сайте
    """
    name = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Пароль еще раз', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, name):
        user = User.query.filter_by(username=name.data).first()
        if user is not None:
            raise ValidationError('Такое имя уже используется')
