from flask import Blueprint, render_template

from app.Models.user import create_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():  # put application's code here
    return render_template('home.html')


@main_bp.route('/message-page')
def profile_page():
    return render_template('message.html')