import unittest
import sqlite3
from database.init_db import create_database

class TestInitDB(unittest.TestCase):

    def test_create_database(self):
        create_database()
        conn = sqlite3.connect('chatbot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='questions';")
        table_exists = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(table_exists)

if __name__ == "__main__":
    unittest.main()
