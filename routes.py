from fastapi import Request, Depends, Form, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND
from starlette.templating import Jinja2Templates

from db.base import engine
from models import Task

templates = Jinja2Templates(directory='templates')


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


router = APIRouter()


@router.get('/')
def home(request: Request, db_session: Session = Depends(get_session)):
    tasks = db_session.query(Task).all()
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'app_name': "Планирование задач",
                                       'task_list': tasks}
                                      )


@router.post('/add')
def add(title: str = Form(...), db_session: Session = Depends(get_session)):
    new_task = Task(title=title)
    db_session.add(new_task)
    db_session.commit()

    url = router.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@router.get('/update/{task_id}')
def update(task_id: int, db_session: Session = Depends(get_session)):
    task = db_session.query(Task).filter(Task.id == task_id).first()
    task.is_complete = not task.is_complete
    db_session.commit()

    url = router.url_path_for('home')

    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)


@router.get('/delete/{task_id}')
def delete(task_id: int, db_session: Session = Depends(get_session)):
    task = db_session.query(Task).filter_by(id=task_id).first()
    db_session.delete(task)
    db_session.commit()

    url = router.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
