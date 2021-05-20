from typing import List

import fastapi

from src.models import ReferenceIn
from src.services import read

router = fastapi.APIRouter()


@router.get('/collections')
def all_collections_view():
    pass


@router.get('/references')
def all_references_view():
    return read.all_references()


@router.post('/references')
def create_references_view(request_objects: List[ReferenceIn]):
    pass