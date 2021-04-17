import os
from pathlib import Path
from dotenv import load_dotenv
import uvicorn
from src.main import configure, api

load_dotenv(Path('.env').resolve())

if os.getenv('DEVELOPMENT'):
    configure()
    uvicorn.run(api, port=8000, host='localhost')
else:  # PRODUCTION
    configure()

