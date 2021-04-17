from pathlib import Path
import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi import Depends

from src.config import Settings
from src.main import get_settings

project_root = Path(__file__).parent.parent.parent
template_path = project_root.joinpath('src', 'templates')
templates = Jinja2Templates(directory=template_path)
router = fastapi.APIRouter()


@router.get('/')
def index(request: Request, settings: Settings = Depends(get_settings())):
    return templates.TemplateResponse('base.html', {'request': request, 'version': settings.version})

