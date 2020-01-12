from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.validators import Required
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class Like(FlaskForm):
    submit = SubmitField('Да!')


class RegistrationForm(FlaskForm):
    name = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Пароль еще раз', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, name):
        user = User.query.filter_by(username=name.data).first()
        if user is not None:
            raise ValidationError('Такое имя уже используется')
