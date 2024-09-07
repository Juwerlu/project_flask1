from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.user.models import User


class LoginForm(FlaskForm):
    """Форма для авторизации."""
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
    """Форма для регистрации."""
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
        validators=[DataRequired(),
                    EqualTo('password', 'Пароли не совпадают!')],
        render_kw={'class': 'form-control'},
        )
    submit = SubmitField(
        'Зарегестрироваться',
        render_kw={'class': 'btn btn-success'},
        )

    def validate_username(self, username):
        """
        Валидатор для проверки создания уже существующего имени пользователя
        при регистрации.
        """
        users_counter = User.query.filter_by(username=username.data).count()
        if users_counter:
            raise ValidationError('Данное имя пользователя уже занято!')

    def validate_email(self, email):
        """Валидатор для проверки уже существующей почты при регистрации."""
        emails_counter = User.query.filter_by(email=email.data).count()
        if emails_counter:
            raise ValidationError('Данное почта уже занята!')
