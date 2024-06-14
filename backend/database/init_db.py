import sqlite3

def create_database():
    """
    Create a SQLite database and a table for storing chatbot interactions.

    The function creates a SQLite database named 'chatbot.db' and a table named 'questions'
    with the following columns:
        - id: An auto-incrementing primary key.
        - question: The user's question (TEXT).
        - response: The chatbot's response (TEXT).
        - language: The language of the conversation (TEXT).
        - timestamp: The timestamp of the interaction (DATETIME, defaults to current timestamp).
        - tag: The intent tag of the question (TEXT).
        - confidence: The confidence score of the predicted tag (REAL).
        - is_out_of_scope: A boolean indicating if the question is out of scope (BOOLEAN).

    If the table already exists, it will not be created again.

    Returns:
        None
    """
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        response TEXT,
        language TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        tag TEXT,
        confidence REAL,
        is_out_of_scope BOOLEAN
    )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database and table created successfully.")
