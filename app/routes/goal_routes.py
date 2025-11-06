from asyncio import Task
from flask import Blueprint, Response, request
from app.models.goal import Goal
from app.routes.route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db


bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    
    return create_model(Goal, request_body)

@bp.post("/<goal_id>/tasks")
def create_goal_associated_with_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    # for task_id in request_body["task_ids"]:
    #     task = validate_model(Task, task_id)
    #     goal.tasks.append(task)
    #     task.goal_id = goal.id

    # db.session.commit()
    
    goal_response = get_tasks_associated_with_a_goal(goal.id)

    return goal_response


@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    
    goal = validate_model(Goal,goal_id)
    return goal.to_dict()



@bp.get("/<goal_id>/tasks")
def get_tasks_associated_with_a_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks = [task.to_dict() for task in goal.tasks]
    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks
    }



@bp.put("/<goal_id>")
def replace_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


