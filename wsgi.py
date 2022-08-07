"""
Entry point for uwsgi.
"""
from src.start import get_app

app = get_app()

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

