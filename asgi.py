import os
import uvicorn

from src.main import configure, application as app, database as db


if os.getenv('PRODUCTION'):
    configure(app, db)
else:  # DEVELOPMENT
    print("Running in DEVELOPMENT mode.")
    configure(app, db)
    uvicorn.run(app, port=8000, host='localhost')
