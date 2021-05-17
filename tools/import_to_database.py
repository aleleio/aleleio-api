"""
A script to write the games library on github (Markdown files with YAML frontmatter) to the database.
See docs/update-games-db.md for more detailed information.
"""
import os
import shutil
from typing import Union
from zipfile import ZipFile
from pathlib import Path

import yaml
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
    download_name = parts[1][9:-4]
    zip_path = tmp_path.joinpath(f'{download_name}.zip')
    open(zip_path, 'wb').write(r.content)
    print(f'Downloaded zip repo to \"{zip_path}\"')

    # Unzip
    with ZipFile(zip_path, 'r') as zip_file:
        zip_file.extractall(tmp_path)

    # Clean Up
    zip_path.unlink()
    print(f'Deleted zip file: \"{zip_path}\"')

    return tmp_path.joinpath(download_name)


def get_files_from_local(path):
    """Create a list of game.md filepaths
    """
    file_list = os.listdir(path)
    file_list = [path.joinpath(file) for file in file_list]
    return file_list


def convert_md_to_game(md) -> Union[GameIn, None]:
    """Convert Markdown to GameIn object
    """
    md = frontmatter.load(md)

    if md.get('alias'):
        return None
    else:
        game = md.to_dict()
        game['names'] = list()
        game['descriptions'] = list()
        game['license_url'] = game['license']['url']
        game['license_owner'] = game['license']['owner']
        game['license_owner_url'] = game['license']['owner_url']
        game['license'] = game['license']['name']
        markdown = mistune.create_markdown(renderer='ast')
        tokens = markdown(game.get('content'))
        is_description = 0
        for token in tokens:
            print('game_md token:', token)
            if token['type'] == 'heading' and token['level'] == 1:
                game['names'].append(token['children'][0]['text'])
                is_description = 0
                continue
            elif token['type'] == 'heading' and token['children'][0]['text'] == 'Description':
                is_description = 1
                continue
            elif is_description > 0:
                if is_description == 1 and not token['type'] == 'list':
                    game['descriptions'].append(token['children'][0]['text'])
                elif is_description > 1:
                    previous_description = game['descriptions'].pop()
                    description = f"{previous_description}\n\n{token['children'][0]['text']}"
                    game['descriptions'].append(description)
                else:
                    # Todo: Make this better. This happens, when the token/paragraph starts with a '1.'
                    game['descriptions'].append(token['children'][0]['children'][0]['children'][0]['text/'])
                is_description += 1

        del game['content']

        return GameIn(**game)


def convert_yml_to_ref(ref_yml):
    """Convert Markdown to reference
    """
    with open(ref_yml, 'r') as fin:
        ymls = yaml.safe_load_all(fin)
        for yml in ymls:
            print(yml)
            # Todo: find refer-to by slug and add reference


def write_games_to_database(games):
    """Use the API functions to validate and insert the games into the database
    Todo: Make sure to update and not touch statistics, metadata etc. in the existing database
    """
    main.configure()
    create.create_game(games)


def run_local():
    project_root = Path(__file__).parent.parent
    local_games_folder = project_root.joinpath('tools', 'games')
    local_refs_folder = project_root.joinpath('tools', 'references')
    games = get_files_from_local(local_games_folder)
    refs = get_files_from_local(local_refs_folder)
    print('Read games & references inside.')
    return games, refs


def run_github():
    download_folder = get_games_from_github()
    download_games_folder = download_folder.joinpath('games')
    download_refs_folder = download_folder.joinpath('references')
    games = get_files_from_local(download_games_folder)
    refs = get_files_from_local(download_refs_folder)
    print('Read games & references inside.')
    return games, refs


if __name__ == '__main__':
    games, refs = run_local()
    # games, refs = run_github()

    for md in games[:2]:
        game = convert_md_to_game(md)
        if game is not None:
            print(game)
            # Todo: write_games_to_database()
            pass
        else:
            print('is alias')

    for ref_yml in refs:
        ref = convert_yml_to_ref(ref_yml)

    # Remove tmp/repo/ folder with games
    # shutil.rmtree(download_folder)

