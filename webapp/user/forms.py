from webapp.user.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя: ',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    password = PasswordField(
        'Пароль: ',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    remember_me = BooleanField(
        'Запомнить меня',
        default=True,
        render_kw={'class': 'form-check-input'},
        )
    submit = SubmitField(
        'Войти',
        render_kw={'class': 'btn btn-success'},
        )


class RegForm(FlaskForm):
    username = StringField(
        'Имя пользователя: ',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    email = StringField(
        'Почта: ',
        validators=[DataRequired(), Email()],
        render_kw={'class': 'form-control'},
        )
    password = PasswordField(
        'Пароль: ',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    password_2 = PasswordField(
        'Подтвердите пароль: ',
        validators=[DataRequired(), EqualTo('password', 'Пароли не совпадают!')],
        render_kw={'class': 'form-control'},
        )
    submit = SubmitField(
        'Зарегестрироваться',
        render_kw={'class': 'btn btn-success'},
        )
    
    def validate_username(self, username):
        users_counter = User.query.filter_by(username=username.data).count()
        if users_counter:
            raise ValidationError('Данное имя пользователя уже занято!')
    def validate_email(self, email):
            emails_counter = User.query.filter_by(email=email.data).count()
            if emails_counter:
                raise ValidationError('Данное почта уже занята!')