"""
A script to write the games library on github (Markdown files with YAML frontmatter) to the database.
See docs/update-games-db.md for more detailed information.
"""
import os
import shutil
from zipfile import ZipFile
from pathlib import Path
from dotenv import load_dotenv

import frontmatter
import mistune
# import repackage
import requests as requests

# repackage.up()

from src.models import GameIn
from src.services import create
from src import main


def get_games_from_github():
    """Download game repository via api.github.com and return filepaths inside.
    """
    project_root = Path(__file__).parent.parent
    load_dotenv(project_root.joinpath('.env'))
    token = os.getenv('GITHUB_TOKEN')
    tmp_path = project_root.joinpath('tools', 'tmp')

    # Download zip file from github
    url = 'https://api.github.com/repos/aleleio/teambuilding-games/zipball'
    headers = {'Authorization': f'token {token}'}
    r = requests.get(url, headers=headers, allow_redirects=True)
    parts = r.headers.get('content-disposition').split(' ')
    file_name = parts[1][9:-4]
    file_path = tmp_path.joinpath(f'{file_name}.zip')
    open(file_path, 'wb').write(r.content)
    print(f'Downloaded zip repo to \"{file_path}\"')

    # Unzip
    with ZipFile(file_path, 'r') as download:
        download.extractall(tmp_path)
    games_path = tmp_path.joinpath(file_name, 'games')

    games = get_games_from_local(games_path)
    print('Read games inside.')

    # Clean Up
    file_path.unlink()
    print(f'Deleted zip file and folder: \"{tmp_path.joinpath(file_name)}\"')

    return games, folder


def get_games_from_local(games_path):
    """Create a list of game.md filepaths
    """
    file_list = os.listdir(games_path)
    file_list = [games_path.joinpath(file) for file in file_list]
    return file_list


def convert_md_to_game(md):
    """Convert Markdown to GameIn object
    """
    print(md)
    md = frontmatter.load(md)

    if md.get('alias'):
        return True, None
    else:
        game = md.to_dict()
        game['names'] = list()
        game['descriptions'] = list()
        markdown = mistune.create_markdown(renderer='ast')
        tokens = markdown(game.get('content'))
        for token in tokens:
            if token['type'] == 'heading' and token['level'] == 1:
                game['names'].append(token['children'][0]['text'])
            elif token['type'] == 'heading':
                is_description = True
                continue
            elif is_description:
                is_description = False
                if token['type'] == 'list':
                    # Todo: This happens, when the description starts with a '1.'
                    game['descriptions'].append(token['children'][0]['children'][0]['children'][0]['text/'])
                else:
                    game['descriptions'].append(token['children'][0]['text'])
        del game['content']

        return False, GameIn(**game)


def write_games_to_database(games):
    """Use the API functions to validate and insert the games into the database
    Todo: Make sure to update and not touch statistics, metadata etc. in the existing database
    """
    main.configure()
    create.create_game(games)


if __name__ == '__main__':
    project_root = Path(__file__).parent.parent
    games_path = project_root.joinpath('tools', 'games')

    # games = get_games_from_local(games_path)
    games, folder = get_games_from_github()
    for md in games:
        is_alias, game = convert_md_to_game(md)

    # Todo: write_games_to_database()

    # Remove tmp/repo/ folder with games
    shutil.rmtree(folder)
