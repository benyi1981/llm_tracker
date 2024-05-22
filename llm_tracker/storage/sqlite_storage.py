import sqlite3
import json
from .storage_backend import StorageBackend

class SQLiteStorage(StorageBackend):
    def __init__(self, config):
        self.db_path = config['sqlite_database']
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage_data (
                    id INTEGER PRIMARY KEY,
                    data TEXT NOT NULL
                )
            ''')
            conn.commit()

    def save(self, data):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usage_data (data) VALUES (?)
            ''', (json.dumps(data),))
            conn.commit()

    def load(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT data FROM usage_data')
            rows = cursor.fetchall()
            return [json.loads(row[0]) for row in rows]

