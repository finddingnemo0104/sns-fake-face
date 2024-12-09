from flask import Blueprint, url_for, redirect, request, render_template
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy.exc import NoResultFound

from app import db
from app.Models.user import User

authentication_bp = Blueprint('authentication', __name__)


@authentication_bp.route('/login', methods=('GET', 'POST'))
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))

    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            user = db.session.execute(
                db.select(User).filter_by(username=username, password=password)
            ).scalar_one()
            login_user(user)
            return redirect(url_for('main.home_page'))
        except NoResultFound:
            return render_template('login.html')
    else:
        return render_template('login.html')


@authentication_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))