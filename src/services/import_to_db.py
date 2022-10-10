import os
import re
from zipfile import ZipFile

import frontmatter
import mistune
import requests
import yaml
from pony.orm import CacheIndexError, db_session

from src.services import create
from src.services.connect_github import get_github_token, get_latest_sha, is_latest_version
from src.start import get_db, ROOT

db = get_db()
TMP = ROOT.joinpath('tmp')


def run_import():
    game_files, ref_files = download_files()

    games, games_with_id, aliases = sort_and_convert_game_files(game_files)
    created, errors = write_games_to_database(games_with_id, games)
    errors += write_aliases_to_database(aliases)

    for yml in ref_files:
        refs = convert_yml_to_ref(yml)
        refs_created, refs_errors = write_references_to_database(refs)

    return {"games": {"len": len(created), "created": [g.id for g in created], "errors": [err.__str__() for err in errors]},
            "refs": {"len": len(refs_created), "created": [r.slug for r in refs_created], "errors": [err.__str__() for err in refs_errors]}}


def sort_and_convert_game_files(game_files):
    games, games_with_id, aliases = [], [], []
    for md in game_files:
        md = frontmatter.load(md)
        if md.get('alias'):
            aliases.append(md)
        else:
            game = convert_md_to_game(md)
            if md.get('id'):
                games_with_id.append(game)
            else:
                games.append(game)
    return games, games_with_id, aliases


def download_files():
    download_folder = import_from_github()
    download_games_folder = download_folder.joinpath('games')
    download_refs_folder = download_folder.joinpath('references')
    games = get_filepaths(download_games_folder)
    refs = get_filepaths(download_refs_folder)
    return games, refs


def import_from_github():
    """Download game repository via api.github.com and return filepaths inside.
    """
    token = get_github_token()
    headers = {'Authorization': f'token {token}'}
    sha = get_latest_sha()

    if is_latest_version(sha):
        return TMP.joinpath(f"aleleio-teambuilding-games-{sha}")

    url = 'https://api.github.com/repos/aleleio/teambuilding-games/zipball'
    r = requests.get(url, headers=headers, allow_redirects=True)
    if r.status_code != 200:
        raise ConnectionError(r.text)
    parts = r.headers.get('content-disposition').split(' ')
    download_name = parts[1][9:-4]

    zip_path = TMP.joinpath(f'{download_name}.zip')
    with open(zip_path, 'wb') as file:
        file.write(r.content)

    # Extract & Clean Up
    with ZipFile(zip_path, 'r') as zip_file:
        zip_file.extractall(TMP)
    zip_path.unlink()

    return TMP.joinpath(download_name)


def get_filepaths(folder_path):
    """Create a list of game.md filepaths
    """
    return [folder_path.joinpath(filename) for filename in os.listdir(folder_path)]


def convert_md_to_game(md):
    """Convert Markdown to game dictionary
    """
    game = md.to_dict()
    game['names'] = list()
    game['descriptions'] = list()

    markdown = mistune.create_markdown(renderer='ast')
    tokens = markdown(game.get('content'))
    for token in tokens:
        md_token_to_game(game, token)

    del game['content']

    return game


def convert_md_to_game_alias(md):
    slug = md.get('alias')
    name = re.search("# (.+?)\n\n", md.content).group(1)
    return slug, name


def md_token_to_game(game, token):
    if is_name(token):
        game['names'].append(token['children'][0]['text'])
    elif is_description(token):
        game['descriptions'].append('')
    elif is_list(token):
        game['descriptions'][-1] += list_to_string(token)
    else:  # is description paragraph
        game['descriptions'][-1] += f"{token['children'][0]['text']}\n\n"


def is_name(token):
    if token['type'] == 'heading' and token['level'] == 1:
        return True
    return False


def is_description(token):
    if token['type'] == 'heading' and token['children'][0]['text'] in ['Description', 'description', 'descr']:
        return True
    return False


def is_list(token):
    """This happens when a paragraph starts with a '1.'
    """
    if token['type'] == 'list':
        return True
    return False


def list_to_string(token):
    result = ''
    for list_item in token['children']:
        result += f"{list_item['children'][0]['children'][0]['text']}\n"
    return f'{result}\n'


def write_games_to_database(*args):
    """Insert the games into the database
    """
    created_total, errors_total = [], []
    for game_list in args:
        created, errors = create.create_games(game_list)
        created_total.extend(created)
        errors_total.extend(errors)
    return created_total, errors_total


@db_session
def write_aliases_to_database(aliases):
    errors = list()
    for md in aliases:
        slug, name = convert_md_to_game_alias(md)
        try:
            game = db.Name.get(slug=slug).game
            create.set_game_names(game, {"names": [name]})
        except CacheIndexError as err:
            errors.append(err)

    return errors


def convert_yml_to_ref(ref_yml):
    """Convert Markdown to reference
    """
    references = []
    with open(ref_yml, 'r') as fin:
        ymls = yaml.safe_load_all(fin)
        for ref in ymls:
            references.append(ref)
    return references


def write_references_to_database(references):
    created, errors = create.create_references(references)
    return created, errors
