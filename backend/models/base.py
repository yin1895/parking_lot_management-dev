from backend.models import db
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
