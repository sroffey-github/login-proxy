from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import datetime
import hashlib
import logging
import sqlite3
import os

load_dotenv()

DB_PATH = os.getenv('DB_PATH')
LOG_PATH = os.getenv('LOG_PATH')

def init():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Users(id INTEGER PRIMARY KEY, Username TEXT, Password TEXT, Role TEXT)')
    conn.commit()
    c.close()
    conn.close()

def create_rotating_log(msg):
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(LOG_PATH, maxBytes=20, backupCount=5)
    logger.addHandler(handler)

    logger.info(f'[{str(datetime.datetime.now())}] {msg}')

def authenticate(usern, passwd):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM Users WHERE Username = ? AND Password = ?', (usern, hashlib.sha256(passwd.encode().hexdigest())))
    results = c.fetchone()
    if results:
        return True
    else:
        return False
