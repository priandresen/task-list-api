from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from typing import Optional
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str] 
    completed_at: Mapped[Optional[datetime]]

    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": False if self.completed_at is None else self.completed_at
        }
    

    # def print_vars(self):
    #     for attribute in vars(self):
    #         print(f"{attribute}: {getattr(self, attribute)}")

    # def to_dict(cls):
    #     for attributes in vars(cls):
    #         getattr(cls, attributes)
#     Similar to the Task model, we should add a class method to the Goal model that initializes a new instance from a dictionary, and use this method in relevant routes.
# If all of our models have this method, we could create a route helper method that initializes a new model instance from a dictionary, and use it in any route that creates a new model instance.

    @classmethod
    def from_dict(cls, data):
        new_task = cls(title=data["title"],
                       description=data["description"],
                       completed_at=data["is_complete"] if "is_complete" in data and data["is_complete"] != False else None
                       )
        return new_task