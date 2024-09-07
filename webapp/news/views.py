from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
)
from flask_login import current_user

from webapp.db import db
from webapp.news.forms import CommentForm
from webapp.news.models import Comment, News
from webapp.weather import get_weather_by_city

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
def index():
    """Функция для главной страницы."""
    title = 'Новости'
    weather = get_weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    all_news = News.query.order_by(News.date.desc()).all()
    return render_template(
        'index.html',
        weather=weather,
        all_news=all_news,
        title=title
        )


@blueprint.route('/news/<int:news_id>')
def single_news(news_id):
    """Функция для страницы отдельной новости."""
    my_news = News.query.filter(News.id == news_id).first()
    if not my_news:
        abort(404)
    form = CommentForm(news_id=news_id)
    return render_template(
        'single_news.html',
        title=my_news.title,
        news=my_news,
        form=form,
    )


@blueprint.route('/news/add-comment', methods=['post'])
def add_comment():
    """Функиця для добавления комментария."""
    form = CommentForm()
    if form.validate_on_submit():
        if News.query.get(form.news_id.data):
            comment = Comment(
                text=form.comment.data,
                news_id=form.news_id.data,
                user_id=current_user.id,
            )
            db.session.add(comment)
            db.session.commit()
            flash('Комментарий отправлен!')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {field}: {error}')
    return redirect(request.referrer)


@blueprint.route('/news/del/<int:id>')
def delete_comment(id):
    """Функция для удаления комментария."""
    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(request.referrer)
