import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment from backend/.env (safe if missing)
_env_path = Path(__file__).with_name('.env')
if _env_path.exists():
    load_dotenv(_env_path)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
