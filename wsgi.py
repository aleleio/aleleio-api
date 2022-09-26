"""
Entry point for uwsgi.
"""
from src.start import get_app, run_startup_tasks, get_db, get_users_db, run_users_startup_tasks

app = get_app()
db = get_db()
udb = get_users_db()

if __name__ == '__main__':
    run_startup_tasks(db)
    run_users_startup_tasks(udb)
    app.run(host='localhost', port=5000)
