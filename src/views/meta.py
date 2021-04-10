import fastapi

router = fastapi.APIRouter()


@router.get('/collections')
def all_collections_view():
    pass
