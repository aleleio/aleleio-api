import fastapi

router = fastapi.APIRouter()


@router.get('/names')
def all_names_view():
    pass


@router.get('/names/{name_id}')
def single_name_view(name_id):
    pass


@router.get('/materials')
def all_materials_view():
    pass


@router.get('/materials/{material_id}')
def single_material_view(material_id):
    pass
