"""
Use GitHub Apps to automatically push changes in the game database to the TB Games repository.

Personal Access Tokens are tied to user accounts and enable full access, while GitHub Apps allows granular permissions.

Helpful:
- https://medium.com/@gilharomri/github-app-bot-with-python-ea38811d7b14
- https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api
"""

from github import GithubIntegration, Github
from github.GithubException import UnknownObjectException
from pony.orm import db_session, desc, select

from src.services.create import slugify
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


def create_multiple_games(games):
    for game in games:
        create_single_game(game)


@db_session
def create_single_game(game):
    repo = connect_to_github()

    cslug, path = get_canonical_slug_and_path(game)
    md = convert_to_markdown(game, cslug)
    repo.create_file(path, message=f"add game \"{cslug}\"", content=md, branch="test")

    # Todo: Rewrite to only send one request instead of n => speedup!
    for name in game.names.select(lambda n: n is not db.Name.get(slug=cslug)):
        path = f"games/{name.slug}.md"
        md = write_alias_to_md(name, cslug)
        repo.create_file(path, message=f"add alias \"{name.slug}\"", content=md, branch="test")


@db_session
def update_single_game(game, request):
    repo = connect_to_github()

    if "names" in request.keys():
        update_names(game, request, repo)

    # Todo: All the rest of the update :)


@db_session
def update_names(game, request, repo):
    """
    Be aware: request["names"] was changed in update.py:update_game_names() and represents only names_new.
    To check against the current canonical name (the name with the lowest ID), the IDs of deleted names can be found
    in request["names_deleted"].
    """
    min_id = get_canonical_name_id(game)

    if request.get("names_deleted"):
        if min_id > min(request["names_deleted"]):
            # canonical name was removed => locate new min_id and update new main file
            slug, path = get_canonical_slug_and_path(game)
            contents = repo.get_contents(path, ref="test")
            md = convert_to_markdown(game, slug)
            repo.update_file(contents.path, message=f"update \"{slug}\"", content=md, sha=contents.sha, branch="test")
        for name in request["names_deleted"]:
            delete_single_file(repo, slugify(name))
    else:
        # only new names => create new aliases
        for name_new in request["names"]:
            name = db.Name.get(full=name_new)
            cname = db.Name[min_id]
            path = f"games/{name.slug}.md"
            md = write_alias_to_md(name, cname.slug)
            repo.create_file(path, message=f"add alias \"{name.slug}\"", content=md, branch="test")


@db_session
def delete_game(game):
    repo = connect_to_github()
    # Todo: Rewrite to only send one request instead of n => speedup!
    for name in game.names.select():
        delete_single_file(repo, name.slug)


def delete_single_file(repo, slug):
    path = f"games/{slug}.md"
    contents = repo.get_contents(path, ref="test")
    repo.delete_file(contents.path, message=f"remove \"{slug}\"", sha=contents.sha, branch="test")


def get_canonical_name_id(game):
    return select(n.id for n in db.Name if n.game is game).min()


def get_canonical_slug_and_path(game):
    min_id = get_canonical_name_id(game)
    name = db.Name[min_id]
    return name.slug, f"games/{name.slug}.md"


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
