import sqlite3
from config import DB_NAME

def get_session():
    db = sqlite3.connect(DB_NAME)
    try:
        yield db
    except:
        raise
        db.close()
