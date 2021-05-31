from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.main import project_root, settings

template_path = project_root.joinpath('src', 'templates')
templates = Jinja2Templates(directory=template_path)
router = APIRouter()


@router.get('/', include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse('base.html', {'request': request, 'version': settings.version})

