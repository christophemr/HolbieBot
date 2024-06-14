import unittest
import sqlite3
from database.view_db import view_database

class TestViewDB(unittest.TestCase):

    def test_view_database(self):
        conn = sqlite3.connect('chatbot.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO questions (question, response, language, tag, confidence, is_out_of_scope) VALUES (?, ?, ?, ?, ?, ?)",
                       ("Test question", "Test response", "en", "test", 0.9, False))
        conn.commit()
        conn.close()

        view_database()
        # This is just to check if the function runs without errors. You can redirect stdout and check the content for a more thorough test.

if __name__ == "__main__":
    unittest.main()
