from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Task
from .extensions import db

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user=current_user).all()
    return render_template('index.html', tasks=tasks)


@main.route('/add', methods=['POST'])
@login_required
def add_task():
    task_description = request.form.get('task_descr').strip()
    if task_description:
        new_task = Task(description=task_description, completed=False, user=current_user)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully.')
    else:
        flash('Task description cannot be empty.')
    return redirect(url_for('main.index'))


@main.route('/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        flash('You do not have permission to modify this task.')
        return redirect(url_for('main.index'))
    task.completed = not task.completed
    db.session.commit()
    flash('Task status updated.')
    return redirect(url_for('main.index'))


@main.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        flash('You do not have permission to modify this task.')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        task_description = request.form.get('task_descr').strip()
        if task_description:
            task.description = task_description
            db.session.commit()
            flash('Task edited successfully.')
            return redirect(url_for('main.index'))
        else:
            flash('Task description cannot be empty.')
    return render_template('edit.html', task_id=task_id, task=task)


@main.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        flash('You do not have permission to delete this task.')
        return redirect(url_for('main.index'))
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.')
    return redirect(url_for('main.index'))
