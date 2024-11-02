from pydantic import BaseModel
from typing import Dict

class TranslationRequest(BaseModel):
    text: str
    language: str
    
class TaskResponse(BaseModel):
    task_id: int
    
class TranslationStatus(BaseModel):
    task_id: int
    status: str
    translation: str
