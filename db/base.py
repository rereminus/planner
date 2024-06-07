import os
from sqlalchemy import create_engine
from config import settings

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
db_path = os.path.join(BASE_DIR, 'db', 'DB')
if not os.path.exists(db_path):
    os.makedirs(db_path)

ur_s = settings.POSTGRES_DATABASE_URLS
engine = create_engine(ur_s, echo=True)
