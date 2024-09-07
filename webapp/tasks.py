from celery import Celery
from celery.schedules import crontab

from webapp import create_app
from webapp.news_ks import get_news_ks

celery_app = Celery('tasks', broker='redis://localhost:6380')
flask_app = create_app()


@celery_app.task
def parse_news():
    with flask_app.app_context():
        print('Собираю новости...')
        get_news_ks()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), parse_news.s())
