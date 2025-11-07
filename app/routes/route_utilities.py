import os
from flask import abort, make_response
from ..db import db
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        invalid = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(invalid , 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def get_models_with_filters(cls, filters=None):

    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    
    if filters and filters.get("sort") == "asc":
        query = query.order_by(cls.title.asc())
    if filters and filters.get("sort") == "desc":
        query = query.order_by(cls.title.desc())

    models = db.session.scalars(query)

    models_response = [model.to_dict() for model in models]

    return models_response

def make_slack_post(cls, model_id):

    task = validate_model(cls, model_id)
    text = f"{cls.__name__} '{task.title}' has been completed!"
    slack_token = os.environ.get("SLACK_TOKEN")
    client = WebClient(token=slack_token)

    try:
        client.chat_postMessage(
            channel="test-slack-api",
            text=text,
        )
    except SlackApiError as e:
        assert e.response["error"]
