import os
from pathlib import Path
from dotenv import load_dotenv
import uvicorn
from src.main import configure, api

if os.getenv('DEVELOPMENT'):
    load_dotenv(Path('.env').resolve())
    configure()
    uvicorn.run(api, port=8000, host='localhost')
else:  # PRODUCTION
    configure()

