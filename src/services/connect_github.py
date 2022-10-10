"""
Note:   GitHub Apps allows granular permissions, Personal Access Tokens grant full access.

Helpful: https://medium.com/@gilharomri/github-app-bot-with-python-ea38811d7b14
         https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api
"""

import os
from functools import cache

import requests
from github import GithubIntegration, Github

from src.start import ROOT

TMP = ROOT.joinpath('tmp')


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


def get_repo():  # pragma: no cover
    gh = Github(get_github_token())
    return gh.get_repo("aleleio/teambuilding-games")


@cache
def get_latest_sha():
    try:
        with open(ROOT.joinpath('.latest-sha'), 'r') as file:
            sha = file.read().strip()
            return sha
    except FileNotFoundError:
        set_latest_sha()
        return get_latest_sha()


def set_latest_sha(sha=None):
    if not sha:
        headers = {'Authorization': f'token {get_github_token()}'}
        url = 'https://api.github.com/repos/aleleio/teambuilding-games/commits?per_page=1'
        r = requests.get(url, headers=headers, allow_redirects=True)
        sha = r.json()[0]["sha"][:7]
    with open(ROOT.joinpath('.latest-sha'), 'w') as file:
        file.write(sha)


def is_latest_version(sha):
    sha_list = [file[-7:] for file in os.listdir(TMP)]
    if sha in sha_list:
        return True
    return False


