from flask import Blueprint, Response, request, abort, make_response
from app.models.task import Task
from ..db import db

tasks_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    
    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body["completed_at"] if "completed_at" in request_body and request_body["completed_at"] != "null" else None

    new_task = Task(title=title, description=description, completed_at=completed_at)
    db.session.add(new_task)
    db.session.commit()

    response = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False if new_task.completed_at is None else new_task.completed_at
    }

    return response, 201

@tasks_bp.get("")
def get_all_tasks():

    query = db.select(Task)

    #if query params, filter by those params


    query = query.order_by(Task.id)

    response = []

    for task in tasks:
        response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False if task.completed_at is None else task.completed_at
        })

    return response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    response = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": False if task.completed_at is None else task.completed_at
    }
    return response

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"message": f"Task {task_id} is invalid"}
        abort(make_response(response, 400))

    query = db.select(Task).where(Task.id == task_id)
    #what is query doing here?
    task = db.session.scalar(query)

    if not task:
        response = {"message": f"Task {task_id} not found"}
        abort(make_response(response, 404))

    return task

@tasks_bp.put("/<task_id>")
def replace_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["is_complete"] if "is_complete" in request_body else None

    db.session.commit()

    return Response(status=204, mimetype="application/json")

