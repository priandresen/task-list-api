from flask import Blueprint, Response, request, abort, make_response
from app.models.task import Task
from app.routes.route_utilities import validate_model
from ..db import db

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201

@bp.get("")
def get_all_tasks():

    query = db.select(Task)

    #if query params, filter by those params

    query = query.order_by(Task.id)

    tasks = db.session.scalars(query.order_by(Task.id))

    task_response = [task.to_dict() for task in tasks]

    return task_response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task,task_id)


    return task.to_dict()

@bp.put("/<task_id>")
def replace_task(task_id):
    task = validate_model(Task,task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["is_complete"] if "is_complete" in request_body else None

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):

    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")