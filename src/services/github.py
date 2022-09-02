"""
Use GitHub Apps to automatically push changes in the game database to the TB Games repository.

Personal Access Tokens are tied to user accounts and enable full access, while GitHub Apps allows granular permissions.

Helpful:
- https://medium.com/@gilharomri/github-app-bot-with-python-ea38811d7b14
- https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api
"""
def push_multiple_games(games):
    for game in games:
        push_single_game(game)


def push_single_game(game):
    # export_to_markdown()
    # connect & push
    pass


def pull_all_games():
    pass
