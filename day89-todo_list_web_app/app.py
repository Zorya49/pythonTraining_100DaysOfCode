# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from sqlalchemy import Integer, String, Boolean, ForeignKey
# from typing import List
# from flask_login import (
#     LoginManager,
#     UserMixin,
#     login_user,
#     login_required,
#     logout_user,
#     current_user,
# )
# from werkzeug.security import generate_password_hash, check_password_hash
#
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret_key_here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.init_app(app)
#
#
# class Base(DeclarativeBase):
#     pass
#
#
# db = SQLAlchemy(model_class=Base)
# db.init_app(app)
#
#
# class User(UserMixin, db.Model):
#     __tablename__ = "user_table"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
#     password_hash: Mapped[str] = mapped_column(String(250), nullable=False)
#     tasks: Mapped[List["Task"]] = relationship(back_populates="user")
#
#
# class Task(db.Model):
#     __tablename__ = "task_table"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     description: Mapped[str] = mapped_column(String(500), nullable=False)
#     category: Mapped[str] = mapped_column(String(500), nullable=False, default='Other')
#     completed: Mapped[bool] = mapped_column(Boolean, nullable=False)
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
#     user: Mapped["User"] = relationship(back_populates="tasks")
#
#
# with app.app_context():
#     db.create_all()
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
#
# @app.route('/')
# @login_required
# def index():
#     tasks = Task.query.filter_by(user=current_user).all()
#     return render_template('index.html', tasks=tasks)
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     if request.method == "POST":
#         username = request.form.get("username").strip()
#         password = request.form.get("password").strip()
#         if not username or not password:
#             flash('Please fill out both fields.')
#             return redirect(url_for('register'))
#         is_existing_user = User.query.filter_by(username=username).first()
#         if is_existing_user:
#             flash('Username already exists.')
#             return redirect(url_for('register'))
#         hashed_password = generate_password_hash(password)
#         new_user = User(username=username, password_hash=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Registration successful. Please log in.')
#         return redirect(url_for('login'))
#     return render_template('register.html')
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#         user = User.query.filter_by(username=username).first()
#         if not user or not check_password_hash(user.password_hash, password):
#             flash('Invalid username or password.')
#             return redirect(url_for('login'))
#         login_user(user)
#         return redirect(url_for('index'))
#     return render_template('login.html')
#
#
# @app.route('/logout', methods=['GET'])
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('index'))
#
#
# @app.route('/add', methods=['POST'])
# @login_required
# def add_task():
#     task_description = request.form.get('task_descr').strip()
#     if task_description:
#         new_task = Task(description=task_description, completed=False, user=current_user)
#         db.session.add(new_task)
#         db.session.commit()
#         flash('Task added successfully.')
#     else:
#         flash('Task description cannot be empty.')
#     return redirect(url_for('index'))
#
#
# @app.route('/complete/<int:task_id>')
# @login_required
# def complete_task(task_id):
#     task = Task.query.get_or_404(task_id)
#     if task.user != current_user:
#         flash('You do not have permission to modify this task.')
#         return redirect(url_for('index'))
#     task.completed = not task.completed
#     db.session.commit()
#     flash('Task status updated.')
#     return redirect(url_for('index'))
#
#
# @app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
# @login_required
# def edit_task(task_id):
#     task = Task.query.get_or_404(task_id)
#     if task.user != current_user:
#         flash('You do not have permission to modify this task.')
#         return redirect(url_for('index'))
#     if request.method == 'POST':
#         task_description = request.form.get('task_descr').strip()
#         if task_description:
#             task.description = task_description
#             db.session.commit()
#             flash('Task edited successfully.')
#             return redirect(url_for('index'))
#         else:
#             flash('Task description cannot be empty.')
#     return render_template('edit.html', task_id=task_id, task=task)
#
#
# @app.route('/delete/<int:task_id>')
# @login_required
# def delete_task(task_id):
#     task = Task.query.get_or_404(task_id)
#     if task.user != current_user:
#         flash('You do not have permission to delete this task.')
#         return redirect(url_for('index'))
#     db.session.delete(task)
#     db.session.commit()
#     flash('Task deleted successfully.')
#     return redirect(url_for('index'))
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
