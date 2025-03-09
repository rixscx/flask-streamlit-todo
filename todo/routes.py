from flask import request, jsonify
from flask_login import login_required, current_user
from todo import app, db
from todo.models import Task

@app.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([{"id": task.id, "task": task.task, "completed": task.completed} for task in tasks])

@app.route('/tasks', methods=['POST'])
@login_required
def add_task():
    data = request.get_json()
    new_task = Task(user_id=current_user.id, task=data['task'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully"}), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"})
    return jsonify({"error": "Task not found"}), 404
