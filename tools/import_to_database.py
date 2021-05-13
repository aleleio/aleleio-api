"""
A script to write the games library on github (Markdown files with YAML frontmatter) to the database.
"""
import os
from pathlib import Path

import frontmatter
import mistune
import repackage

repackage.up()

from src.models import GameIn
from src.services import create
from src import main


def get_games_from_github():
    """Access game repository via api.github.com
    """
    games = []
    return games


def get_games_from_local():
    project_root = Path(__file__).parent.parent
    games_path = project_root.joinpath('tools', 'games')
    file_list = os.listdir(games_path)
    print(file_list)
    return file_list


def convert_md_to_game(md):
    """
    """
    md = frontmatter.load('tools/games/' + md + '.md')

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
                game['descriptions'].append(token['children'][0]['text'])
        del game['content']
        print('game:', game)

        return False, GameIn(**game)



def write_games_to_database():
    """Use the API functions to validate and insert the games into the database
    """
    main.configure()
    create.create_game(games_list)


if __name__ == '__main__':
    games = get_games_from_local()
    # games = get_games_from_github()
    # for md in games:
    #     is_alias, game = convert_md_to_game(md)

