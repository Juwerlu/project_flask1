from flask import Blueprint, flash, redirect, url_for, render_template
from webapp.user.models import User
from webapp.db import db
from flask_login import current_user, login_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/cabinet')
@login_required
def cabinet():
    if current_user.status == 'admin':
        all_inf = User.query.all()
        return render_template(
            'cabinet.html',
            all_inf=all_inf,
            )
    return 'Ты не админ, свяжись с админом!'


@blueprint.route('/change-status/<int:id><string:status>')
def changed_status(id, status):
    user = User.query.get(id)
    user.status = status
    db.session.commit()
    return redirect(url_for('admin.cabinet'))


@blueprint.route('/del/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.cabinet'))
