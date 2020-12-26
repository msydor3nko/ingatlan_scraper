import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

DATABASE_CONNECTION = os.environ.get("DATABASE_CONNECTION")

DATA_STORAGE_SETTINGS = "db"  # or "csv"