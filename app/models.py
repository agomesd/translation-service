from sqlalchemy import Column, Integer, String, Text, JSON

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TranslationTask(Base):
    __tablename__ = "translation_tasks"
    
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    language = Column(Text, nullable=False)
    status = Column(String, default="in progress")
    
    translation = Column(JSON, default={})
