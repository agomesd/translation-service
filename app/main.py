from fastapi import FastAPI, Request, BackgroundTasks, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import schemas
import crud
import models
import utils
from database import get_db, engine
import logging
logger = logging.getLogger("uvicorn.error")

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", { "request": request })


@app.post("/translate", response_model=schemas.TaskResponse)
def translate(request: schemas.TranslationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    task = crud.create_translation_task(db, request.text, request.language)
    logger.info(f"TASK ID: {task.id}")
    background_tasks.add_task(utils.translate_text, task.id, request.text, request.language, db)
    return {"task_id": int(task.id)}
    
    
@app.get("/translate/{task_id}", response_model=schemas.TranslationStatus)
def get_translation(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return {"task_id": task_id, "status": task.status, "translation": task.translation}
    
@app.get("/translate/content/{task_id}", response_model=schemas.TranslationStatus)
def get_translation_content(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return {task}
