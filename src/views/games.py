def get_all():
    return {"games": "all"}


def create():
    return "create", 201


def get_single(game_id):
    return f"get_single, id {game_id}"


def update_single():
    return "update_single"


def delete_single():
    return "delete_single"