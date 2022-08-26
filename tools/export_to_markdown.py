"""
A couple of scripts to export JSON or Python objects to Markdown, using the API's GameIn model.
"""

import json

from src.services.create import slugify


def convert_json_to_dict():
    """Convert JSON output from api-legacy to GameIn model.
    Probably only needed for initial transfer of games.
    """
    json_file = open('dumps/2021-05-13-dump.json')
    json_str = json_file.read()
    data = json.loads(json_str)

    games = []
    for g in data:
        gl_substitute = {'10': 'short', '30': 'medium', '120': 'long'}
        gn_substitute = {'names': 'first', 'ener': 'energy', 'hon': 'honesty', 'strat': 'strategy', 'insp': 'inspiration', 'why': 'why', 'id': 'identity'}
        game = dict(
            names=[n['text'] for n in g['name']],
            descriptions=[d['text'] for d in g['description']],
            materials=g['material'],
            game_types=g['game_type'],
            game_lengths=[gl_substitute[i] for i in g['game_length']],
            group_sizes=g['group_size'],
            group_needs=[{"slug": gn_substitute[k], "score": v} for k, v in g['group_needs'].items()],
            prior_prep=g['prior_prep'] if g['prior_prep'] else None,
            exhausting=g['exhausting'],
            touching=g['touching'],
            scalable=g['scalable'],
            license={},
        )
        games.append(game)
    return games


def write_dict_to_md(game):
    """Create a Markdown file with YAML frontmatter for each unique game.
    Store by slug of first name, all other names for the same game are only created as reference aliases.
    """

    md = ['---']
    md = add_categories(game, md)
    md = add_group_needs(game, md)
    md = add_materials(game, md)
    md = add_prior_prep(game, md)
    md = add_bools(game, md)
    md = add_license(game, md)
    md.append('---')
    md.append(f"# {game['names'][0]}\n")
    for d in game['descriptions']:
        md.append('## Description')
        md.append(f'{d}\n')
    md = str.join('\n', md)

    slug = slugify(game['names'][0])
    filepath = 'games/' + slug + '.md'
    with open(filepath, 'w') as fin:
        fin.write(md)

    return slug, game['names'].pop(0)


def add_categories(game, md):
    for category in ['game_types', 'game_lengths', 'group_sizes']:
        md.append(f'{category}:')
        for item in game[category]:
            md.append(f'  - {item}')
    return md


def add_group_needs(game, md):
    if game['group_needs']:
        md.append('group_needs:')
        for gn in game['group_needs']:
            md.append(f"  - slug: {gn['slug']}")
            md.append(f"    score: {gn['score']}")

    return md


def add_materials(game, md):
    if game['materials']:
        md.append('materials:')
        for m in game['materials']:
            clean_m = m.replace('"', '\\"')
            md.append(f'  - \"{clean_m}\"')
    return md


def add_prior_prep(game, md):
    if game['prior_prep']:
        clean_pp = game['prior_prep'].replace('"', '\\"')
        md.append(f'prior_prep: \"{clean_pp}\"')
    return md


def add_bools(game, md):
    md.append(f"exhausting: {game['exhausting']}")
    md.append(f"touching: {game['touching']}")
    md.append(f"scalable: {game['scalable']}")
    if game.get('digital'):
        md.append(f"digital: {game['digital']}")
    else:
        md.append(f"digital: no")
    return md


def add_license(game, md):
    if game.get('license'):
        md.append(f"license:")
        md.append(f"  name: {game['license.name']}")
        md.append(f"  url: {game['license.url']}")
        md.append(f"  owner: {game['license.owner']}")
        md.append(f"  owner_url: {game['license.owner_url']}")
    return md


def write_alias_to_md(game, root_name: tuple):
    """Create a minimal Markdown file with YAML frontmatter, referencing the actual game file/object
    """
    root_slug, root_full = root_name
    md = ['---']
    md.append(f'alias: {root_slug}')
    md.append('---')
    md.append(f"# {game['names'][0]}\n")
    md.append(f"Alias for [{root_full}]({root_slug}.md).")
    md = str.join('\n', md)

    slug = slugify(game['names'][0])
    filepath = 'games/' + slug + '.md'
    with open(filepath, 'w') as fin:
        fin.write(md)

    game['names'].pop(0)


if __name__ == '__main__':
    # Todo: Figure out from where to stream the data
    games = convert_json_to_dict()
    for game in games:
        root_name = write_dict_to_md(game)
        while len(game['names']) > 0:
            write_alias_to_md(game, root_name)
