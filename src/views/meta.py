from typing import List

import fastapi
from pony.orm import db_session

from src.models import ReferenceIn, Reference, ReferenceOut

router = fastapi.APIRouter()


@router.get('/collections')
def all_collections_view():
    pass


@router.get('/references')
def all_references_view():
    with db_session:
        references = Reference.select()
        result = [ReferenceOut.from_orm(r) for r in references]
    return result


@router.post('/references')
def create_references_view(request_objects: List[ReferenceIn]):
    pass