from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str] 
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True, default=None)
    #is completed at correct? I want it to be default none unles specified with datatime
    # If completed_at is not provided, it should default to None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": False if self.completed_at is None else self.completed_at
        }
    
    def from_dict(self, data):
        self.title = data.get("title", None)
        self.description = data.get("description", None)
        self.completed_at = data.get("is_complete", None)
        
        return self
    
    #update from dict method?
    
