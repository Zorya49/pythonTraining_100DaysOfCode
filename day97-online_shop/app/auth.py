from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .extensions import db, login_manager

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == "POST":
        name = request.form.get("name").strip()
        surname = request.form.get("surname").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        if not email or not password:
            flash('Please fill out email and password fields.')
            return redirect(url_for('auth.register'))
        is_existing_user = User.query.filter_by(email=email).first()
        if is_existing_user:
            flash('Account for this email already exists.')
            return redirect(url_for('auth.login'))
        new_user = User(name=name, surname=surname, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('main.product_list'))
    return render_template('login.html')


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
