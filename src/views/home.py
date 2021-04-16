import os
from pathlib import Path
import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates

project_root = Path(__file__).parent.parent.parent
template_path = project_root.joinpath('src', 'templates')
templates = Jinja2Templates(directory=template_path)
router = fastapi.APIRouter()


@router.get('/')
def index(request: Request):
    return templates.TemplateResponse('base.html', {'request': request, 'version': os.getenv('VERSION')})

