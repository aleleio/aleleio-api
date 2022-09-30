import os
from functools import cache
from zipfile import ZipFile

import frontmatter
import mistune
import requests
import yaml
from github import GithubIntegration

from src.services import create
from src.services.export_to_repo import set_latest_sha
from src.start import get_db, ROOT

db = get_db()
TMP = ROOT.joinpath('tmp')


def run_import():
    game_files, ref_files = download_files()

    game_list = list()
    alias_list = list()
    for md in game_files:
        game = convert_md_to_game(md)
        if game:
            game_list.append(game)
        else:
            alias_list.append(md)
    games_created, games_errors = write_games_to_database(game_list)

    for yml in ref_files:
        refs = convert_yml_to_ref(yml)
        refs_created, refs_errors = write_references_to_database(refs)

    return {"games": {"len": len(games_created), "created": [g.id for g in games_created], "errors": games_errors},
            "refs": {"len": len(refs_created), "created": [r.slug for r in refs_created], "errors": refs_errors}}


def download_files():
    download_folder = import_from_github()
    download_games_folder = download_folder.joinpath('games')
    download_refs_folder = download_folder.joinpath('references')
    games = get_filepaths(download_games_folder)
    refs = get_filepaths(download_refs_folder)
    return games, refs


@cache
def get_latest_sha():
    try:
        with open(ROOT.joinpath('.latest-sha'), 'r') as file:
            sha = file.read().strip()
            return sha
    except FileNotFoundError:
        set_latest_sha()
        return get_latest_sha()


def get_github_token():
    try:
        with open(ROOT.joinpath('gamebot-private-key.pem')) as cert_file:
            bot_key = cert_file.read()
        bot = GithubIntegration(233902, bot_key)
        token = bot.get_access_token(bot.get_installation('aleleio', 'teambuilding-games').id).token
    except FileNotFoundError as err:
        token = os.environ.get('GITHUB')
        if not token:
            raise FileNotFoundError("Have you added a GitHub Personal Access Token to .env?")
    return token


def import_from_github():
    """Download game repository via api.github.com and return filepaths inside.
    """
    token = get_github_token()
    headers = {'Authorization': f'token {token}'}
    sha = get_latest_sha()

    if is_latest_version():
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


def is_latest_version():
    latest_sha = get_latest_sha()
    sha_list = [file[-7:] for file in os.listdir(TMP)]
    if latest_sha in sha_list:
        return True
    return False


def get_filepaths(folder_path):
    """Create a list of game.md filepaths
    """
    return [folder_path.joinpath(filename) for filename in os.listdir(folder_path)]


def convert_md_to_game(md):
    """Convert Markdown to game dictionary
    """
    md = frontmatter.load(md)

    if md.get('alias'):
        return None

    game = md.to_dict()
    game['names'] = list()
    game['descriptions'] = list()

    markdown = mistune.create_markdown(renderer='ast')
    tokens = markdown(game.get('content'))
    for token in tokens:
        md_token_to_game(game, token)

    del game['content']

    return game


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


def write_games_to_database(games):
    """Insert the games into the database
    Todo: Make sure to update and not touch statistics, metadata etc. in the existing database
    """
    created, errors = create.create_games(games)
    return created, errors


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
