from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from webapp.db import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.String(8), default='user')
    email = db.Column(db.String)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'User {self.id}: {self.username}: {self.status}'
