from flask import Blueprint, Response, request
from app.models import task
from app.models.goal import Goal
from app.routes.route_utilities import validate_model, create_model, get_models_with_filters, make_slack_post
from ..db import db
from datetime import datetime

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    
    goal = validate_model(Goal,goal_id)
    return goal.to_dict()

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

# @bp.patch("/<goal_id>/mark_complete")
# def patch_goal(goal_id):
#     task = validate_model(Task, task_id)
#     task.completed_at = datetime.now()
#     make_slack_post(Task, task_id)

#     db.session.commit()
#     return Response(status=204, mimetype="application/json")

# @bp.patch("/<task_id>/mark_incomplete")
# def patch_incomplete_task(task_id):
#     task = validate_model(Task, task_id)
#     task.completed_at = None

#     db.session.commit()
#     return Response(status=204, mimetype="application/json")




