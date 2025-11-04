from flask import Blueprint, Response, request
from app.models.task import Task
from app.routes.route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    
    return create_model(Task, request_body)

@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)

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