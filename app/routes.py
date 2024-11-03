from flask import Blueprint, render_template, request
from sqlalchemy.exc import NoResultFound

from app import db
from app.Models.user import create_user, User

main_bp = Blueprint('main', __name__)
authentication_bp = Blueprint('authentication', __name__)


@main_bp.route('/')
def home():  # put application's code here
    return render_template('login.html')


@main_bp.route('/message')
def message_page():
    return render_template('message.html')


@main_bp.route('/home')
def home_page():
    return render_template('home.html')


@authentication_bp.route('/login', methods=('GET', 'POST'))
def login_page():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            user = db.session.execute(
                db.select(User).filter_by(username=username, password=password)
            ).scalar_one()
            return render_template('home.html')
        except NoResultFound:
            return render_template('login.html')
    else:
        return render_template('login.html')
