# Contributing to alele.io | API Component

Welcome to alele.io! 

### Set up your local development environment:

**Step 1: Python Version** \
We are using pyenv ([linux](https://github.com/pyenv/pyenv) [mac](https://github.com/pyenv/pyenv) [win](https://github.com/pyenv-win/pyenv-win)) for Python version management.
Either check if you want to do the same or install the version specified in [.python-version](.python-version) for your operating system: [installation guide](https://realpython.com/installing-python/).

**Step 2: Virtual Environment** \
To separate the local python packages from the system python's packages, you want to set up a virtual environment
for the project. Create it with python's `venv` module in the project root, activate it and `pip` install
the requirements. Either with bash on a Unix system:
    
    $ cd ~/code/aleleio-api
    $ python -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt
    (venv) $

Or with the Command Prompt/PowerShell:

    cd code\aleleio-api
    python -m venv venv
    .\venv\Scripts\activate
    (venv) pip install -r requirements.txt
    (venv)

Deactivate the virtual environment at any time with `deactivate`.

**Step 3: Configuration**
Copy the provided [.env_template](.env_template) and rename it to `.env`, to set up the neccessary environment variables
(envars) for development.

**Step 4: Games (optional)**
To load the most recent collection of games into your database, add a [github token](https://github.com/settings/tokens)
to your [.env](.env_template) file and run the [import script](tools/import_to_database.py) in [tools/](tools).


## Workflow

We are using [github flow](https://guides.github.com/introduction/flow/), Pull Requests (PRs) are welcome.

The changelog and future roadmap can be found in [ROADMAP.md](ROADMAP.md).
