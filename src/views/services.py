from flask import Blueprint

from src.services.import_to_db import import_from_github, latest_version_exists

bp = Blueprint('services', __name__)


@bp.route('/test')
def test_me():

    game_files, ref_files = run_github()

    run_startup_tasks(get_db())

    game_list = []
    alias_list = []
    for md in game_files:
        game = convert_md_to_game(md)
        if game:
            game_list.append(game)
        else:
            alias_list.append(md)

    print()
    print('Writing games to database')
    write_games_to_database(game_list)

    print()
    print('Writing references to database')
    for yml in ref_files:
        print(f"Reading from: {str(yml).split('/').pop()}")
        refs = convert_yml_to_ref(yml)
        write_references_to_database(refs)
    result = latest_version_exists()
    return {"result": result}
