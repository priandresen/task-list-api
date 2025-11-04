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

    @classmethod
    def from_dict(cls, data):
        new_task = cls(title=data["title"],
                       description=data["description"],
                       completed_at=data["is_complete"] if "is_complete" in data and data["is_complete"] != False else None
                       )
        return new_task
    
