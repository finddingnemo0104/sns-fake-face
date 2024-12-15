import traceback
from datetime import datetime

from flask import Blueprint, url_for, redirect, request, render_template, flash
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy.exc import NoResultFound, IntegrityError

from app import db, login_manager
from app.Models.user import User

authentication_bp = Blueprint('authentication', __name__)


# Custom login required function
# function to check if a user is logged in
# if not logged in, redirect to login page
# if logged in, return the user
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('authentication.login_page'))


@authentication_bp.route('/login', methods=('GET', 'POST'))
def login_page():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            user = db.session.execute(
                db.select(User).filter_by(username=username, password=password)
            ).scalar_one()
            login_user(user)
            return redirect(url_for('main.home'))
        except NoResultFound:
            return render_template('login.html')
    else:
        return render_template('login.html')


@authentication_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        errors = {}
        try:
            username = request.form.get('username', '').strip()
            name = request.form.get('name', '').strip()
            dob = request.form.get('dob', '').strip()
            gender = request.form.get('gender', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            rePassword = request.form.get('re-password', '').strip()
            # Validation
            if not username:
                errors['username'] = 'Tên đăng nhập không được để trống.'
            if not name:
                errors['name'] = 'Tên hiển thị không được để trống.'
                if not name.isalpha() and not all(c.isalpha() or c == "'" for c in name):
                    errors['name'] = "Tên hiển thị chỉ được bao gồm chữ cái và dấu '."
            if not dob:
                errors['dob'] = "Vui lòng chọn ngày sinh hợp lệ."
            else:
                dob_date = datetime.strptime(dob, '%Y-%m-%d')
                today = datetime.today()
                age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
                if age < 13:
                    errors['dob'] = "Bạn phải đủ 13 tuổi để đăng ký."
                elif age > 150:
                    errors['dob'] = "Ngày sinh không hợp lệ. Vui lòng kiểm tra lại."
            if gender not in ['male', 'female', 'other']:
                errors['gender'] = 'Bạn phải chọn giới tính.'
            if not email:
                errors['email'] = 'Email không được để trống.'
            elif '@' not in email or '.' not in email:
                errors['email'] = 'Email không hợp lệ.'
            if not password or len(password) < 8 or not any(c.islower() for c in password) or not any(
                    c.isupper() for c in password) or not any(c.isdigit() for c in password) or not any(
                c in "!@#$%^&*()-_+=<>?/{}~" for c in password):
                errors[
                    'password'] = 'Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ thường, chữ hoa, chữ số và ký tự đặc biệt.'
            if password != rePassword:
                errors['re_password'] = 'Mật khẩu không khớp.'

            # Nếu có lỗi, render lại form với lỗi
            if errors:
                return render_template('register.html', errors=errors, form_data=request.form)

            dob = datetime.strptime(dob, '%Y-%m-%d')
            # Tạo người dùng mới
            user = User(username=username, password=password, name=name, gender=gender,
                        avatar="/static/image/no-avatar.jpg", cover=None, dob=dob, biography=None,
                        email=email, created_at=datetime.now(),
                        updated_at=datetime.now())
            db.session.add(user)
            db.session.commit()
            flash('Đăng ký thành công! Bạn có thể đăng nhập.', 'success')
            return redirect(url_for('main.home'))
        except IntegrityError as e:
            traceback.print_exc()
            db.session.rollback()
            errors['username'] = 'Tên đăng nhập hoặc email đã tồn tại.'
            return render_template('register.html', errors=errors, form_data=request.form)
        except Exception as e:
            errors['general'] = 'Đã xảy ra lỗi. Vui lòng thử lại sau.'
            return render_template('register.html', errors=errors, form_data=request.form)
    else:
        return render_template('register.html', form_data=request.form)


@authentication_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
