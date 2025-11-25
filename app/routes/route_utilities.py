import os
from flask import abort, json, make_response
import requests
from ..db import db
import os

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

    model = validate_model(cls, model_id)

    url= "https://slack.com/api/chat.postMessage"

    text = f"{cls.__name__} '{model.title}' has been completed!"
    slack_token = os.environ.get("SLACK_TOKEN")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{slack_token}"
    }
    payload = json.dumps({
        "channel": "C09N95RPR34",
        "text": text
    })

    url = "https://slack.com/api/chat.postMessage"


    response = requests.request("POST", url, headers=headers, data=payload)
    
