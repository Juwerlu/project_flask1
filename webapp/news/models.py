from datetime import datetime

from sqlalchemy.orm import relationship

from webapp.db import db


class News(db.Model):
    """Модель для новостей."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime)
    text = db.Column(db.Text, nullable=True)

    def comments_count(self):
        return Comment.query.filter(Comment.news_id == self.id).count()


class Comment(db.Model):
    """Модель для комментариев."""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

    news_id = db.Column(
        db.Integer,
        db.ForeignKey('news.id', ondelete='CASCADE'),
        index=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        index=True,
    )

    news = relationship('News', backref='comments')
    user = relationship('User', backref='comments')
