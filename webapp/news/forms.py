from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from webapp.news.models import News


class CommentForm(FlaskForm):
    """Форма для комментариев."""
    news_id = HiddenField('ID новости', validators=[DataRequired()])
    comment = StringField(
        'Оставьте комментарий:',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    submit = SubmitField(
        'Отправить',
        render_kw={'class': 'btn btn-primary'},
    )

    def validate_news_id(self, news_id):
        """
        Валидатор для проверки попытки оставить комментарий
        к несуществующей новости.
        """
        if not News.query.get(news_id.data):
            raise ValidationError('Новость была удалена!')
