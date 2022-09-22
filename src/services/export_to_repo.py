"""
Export games to teambuilding-games repository on GitHub.

Note:   GitHub Apps allows granular permissions, Personal Access Tokens grant full access.

Helpful: https://medium.com/@gilharomri/github-app-bot-with-python-ea38811d7b14
         https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api
"""

from github import GithubIntegration, Github, InputGitTreeElement, Repository
from pony.orm import db_session, select

from src.start import get_project_root, get_db

db = get_db()


def connect_to_github():
    root = get_project_root()
    with open(root.joinpath('gamebot-private-key.pem')) as cert_file:
        bot_key = cert_file.read()
    bot = GithubIntegration(233902, bot_key)
    token = bot.get_access_token(bot.get_installation('aleleio', 'teambuilding-games').id).token
    gh = Github(token)
    return gh.get_repo("aleleio/teambuilding-games")


@db_session
def create_multiple_games(games: list[db.Game]):
    file_list = list()
    cslug_list = list()
    for game in games:
        cname = get_canonical_name_obj(game)
        cslug_list.append(cname.slug)
        md = convert_to_markdown(game, cname.slug)
        file_list.append(dict(md=md, slug=cname.slug))
        file_list.extend(create_aliases(game, cname))
    all_cslugs = ', '.join(f'"{ms}"' for ms in cslug_list)
    commit_multiple(connect_to_github(), file_list, message=f"create {all_cslugs}")


def create_aliases(game: db.Game, cname: db.Name):
    file_list = list()
    for name in game.names.select(lambda n: n is not cname):
        md = write_alias_to_md(name, cname.slug)
        file_list.append(dict(md=md, slug=name.slug))
    return file_list


@db_session
def update_single_game(game: db.Game, request: dict):
    """Export updated .md files to teambuilding-games repo.
    At this point, all patched changes are already committed to the db.Game object.
    """
    name = get_canonical_name_obj(game)

    if "names" in request.keys() or "names_deleted" in request.keys():
        file_list = update_names(game, request)
    else:
        file_list = [dict(md=convert_to_markdown(game, name.slug), slug=name.slug)]

    commit_multiple(connect_to_github(), file_list, message=f"update \"{name.slug}\"")


@db_session
def update_names(game: db.Game, request: dict):
    """Update main game file in repo and create or delete alias files.
    Be aware: request["names"] was changed in update.py:update_game_names() and represents only names_new.
    To check against the current canonical name (the name with the lowest ID), the IDs of deleted names can be found
    in request["names_deleted"].
    """
    min_id = get_canonical_name_id(game)
    cname = get_canonical_name_obj(game)
    file_list = list()

    if request.get("names_deleted"):
        if min_id > min(n['id'] for n in request["names_deleted"]):
            # canonical name was removed => locate new min_id and update new main file
            file_list.append(dict(md=convert_to_markdown(game, cname.slug), slug=cname.slug))
        for name in request["names_deleted"]:
            file_list.append(dict(slug=name['slug'], delete=True))
    if request.get("names"):
        # create new aliases
        file_list.extend(create_aliases(game, cname))

    return file_list


@db_session
def delete_game(game):
    name = get_canonical_name_obj(game)
    payload = [dict(slug=name.slug, delete=True) for name in game.names.select()]
    commit_multiple(connect_to_github(), payload, message=f"delete \"{name.slug}\"")


def get_canonical_name_id(game):
    return select(n.id for n in db.Name if n.game is game).min()


def get_canonical_name_obj(game):
    min_id = get_canonical_name_id(game)
    return db.Name[min_id]


def commit_multiple(repo, file_list, message="update games"):
    element_list = list()
    for content in file_list:
        if content.get('delete'):
            blob_sha = None
        else:
            blob = repo.create_git_blob(content['md'], "utf-8")
            blob_sha = blob.sha
        el = InputGitTreeElement(path=f"games/{content['slug']}.md", mode="100644", type="blob", sha=blob_sha)
        element_list.append(el)

    branch_sha = repo.get_branch("test").commit.sha
    base_tree = repo.get_git_tree(sha=branch_sha)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(sha=branch_sha)
    commit = repo.create_git_commit(message, tree, [parent])
    branch_refs = repo.get_git_ref("heads/test")
    branch_refs.edit(sha=commit.sha)


def convert_to_markdown(game, slug):
    """Create a Markdown file with YAML frontmatter.
    Store by slug of first name, all other names for the same game are only created as reference aliases.
    """
    name = db.Name.get(slug=slug)
    md = ["---"]
    md = add_categories(game, md)
    md = add_group_needs(game, md)
    md = add_materials(game, md)
    md = add_prior_prep(game, md)
    md = add_bools(game, md)
    md = add_license(game, md)
    md.append("---")
    md.append(f"# {name.full}")
    for d in game.descriptions:
        md.append("## Description")
        md.append(f"{d.text}\n")
    md = str.join('\n', md)
    return md


def add_categories(game, md):
    for category in ["game_types", "game_lengths", "group_sizes"]:
        md.append(f"{category}:")
        for item in getattr(game, category).select():
            md.append(f"  - {item.slug}")
    return md


def add_group_needs(game, md):
    if game.group_need_scores.select().exists():
        md.append("group_needs:")
        for gns in game.group_need_scores.select():
            md.append(f"  - slug: {gns.group_need.slug}")
            md.append(f"    score: {gns.value}")
    return md


def add_materials(game, md):
    if game.materials.select().exists():
        md.append('materials:')
        for m in game.materials.select():
            md.append(f'  - \"{m.slug}\"')
    return md


def add_prior_prep(game, md):
    if game.prior_prep:
        # clean_pp = game['prior_prep'].replace('"', '\\"')
        md.append(f'prior_prep: \"{game.prior_prep}\"')
    return md


def add_bools(game, md):
    md.append(f"exhausting: {game.exhausting}")
    md.append(f"touching: {game.touching}")
    md.append(f"scalable: {game.scalable}")
    if game.digital:
        md.append(f"digital: {game.digital}")
    else:
        md.append(f"digital: no")
    return md


def add_license(game, md):
    md.append(f"license:")
    md.append(f"  name: {game.license.name}")
    md.append(f"  url: {game.license.url}")
    md.append(f"  owner: {game.license.owner}")
    md.append(f"  owner_url: {game.license.owner_url}")
    return md


def write_alias_to_md(name, cslug):
    """Create a minimal Markdown file with YAML frontmatter, referencing the actual game file/object
    """
    md = ["---"]
    md.append(f"alias: {cslug}")
    md.append("---")
    md.append(f"# {name.slug}\n")
    md.append(f"Alias for [{cslug}.md]({cslug}.md).")
    md = str.join('\n', md)
    return md
