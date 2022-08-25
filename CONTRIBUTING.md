# Contributing to alele.io | API Component

The API Component uses Python 3.10 to run our stack:

* API-first design driven by [Connexion](https://github.com/spec-first/connexion) with [Flask](https://flask.palletsprojects.com)
* open standards using [OpenAPI Specification 3.0](https://openapis.org)
* database access through [PonyORM](https://ponyorm.org/)
* templates are written with [Jinja](https://jinja.palletsprojects.com/)
* testing with [pytest](https://docs.pytest.org)

## Setting Up the Local Development Environment

**Python Version** \
We are using pyenv [linux](https://github.com/pyenv/pyenv) [mac](https://github.com/pyenv/pyenv) [win](https://github.com/pyenv-win/pyenv-win] for Python version management.
Either check if you want to do the same or install the version specified in [.python-version](.python-version) for your operating system: [guide to installation](https://realpython.com/installing-python/).

**Virtual Environment** \
To separate the local python packages from the system python's packages, you want to set up a virtual environment
for the project. Create it with python's `venv` module in the project root, activate it and `pip` install
the requirements. Either with bash on a Unix system:
    
    [kitabonga@bash]$ cd ~/code/aleleio-api
    [kitabonga@bash]$ python -m venv venv
    [kitabonga@bash]$ source venv/bin/activate
    (venv)[kitabonga@bash]$ pip install -r requirements.txt
    (venv)[kitabonga@bash]$

Or with the Command Prompt/PowerShell:

    C:\Users\kitabonga> cd code/aleleio-api
    C:\Users\kitabonga\code\aleleio-api>python -m venv venv
    C:\Users\kitabonga\code\aleleio-api>.\venv\Scripts\activate
    (venv) C:\Users\kitabonga\code\aleleio-api> pip install -r requirements.txt
    (venv) C:\Users\kitabonga\code\aleleio-api>

Deactivate the virtual environment at any time with `deactivate`.

**Configuration**
Copy the provided [.env_template](.env_template) and rename it to `.env`, to set up the neccessary environment variables
(envars) for development.


## Workflow

*Todo: Document the workflow*

We are using [github flow](https://guides.github.com/introduction/flow/).

If you want to better understand how the code works, look at the [/docs folder](docs/README.md).

The changelog and future roadmap can be found in [ROADMAP.md](ROADMAP.md).
