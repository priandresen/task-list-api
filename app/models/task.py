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
    
