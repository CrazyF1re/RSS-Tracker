import sqlite3
import os
from DataCollection.collection import Database

def get_session():
    db = Database()
    try:
        yield db
    except:
        raise


def put_data():
    pass

def del_data():
    pass