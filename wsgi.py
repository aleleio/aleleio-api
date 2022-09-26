"""
Entry point for uwsgi.
"""
from src.start import get_app, run_startup_tasks, get_db

app = get_app()
db = get_db()
udb = get_db(users_db=True)

if __name__ == '__main__':
    run_startup_tasks(db)
    run_startup_tasks(udb)
    app.run(host='localhost', port=5000)
