import sqlite3

def view_database():
    """
    Connects to the 'chatbot.db' database, fetches all records from the 'questions' table,
    and prints out each record's details in a formatted manner.
    """
    # Connect to the SQLite database named 'chatbot.db'
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()

    # Execute an SQL query to select all records from the 'questions' table
    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()  # Fetch all the results of the query

    # Iterate over each row in the results
    for row in rows:
        print(f"ID: {row[0]}")            # Print the ID of the record
        print(f"Question: {row[1]}")      # Print the question text
        print(f"Response: {row[2]}")      # Print the response text
        print(f"Language: {row[3]}")      # Print the language of the question/response
        print(f"Timestamp: {row[4]}")     # Print the timestamp when the record was created
        print(f"Tag: {row[5]}")           # Print the tag associated with the question
        print(f"Confidence: {row[6]}")    # Print the confidence score of the prediction
        print(f"Is Out of Scope: {row[7]}")  # Print whether the question was out of scope
        print("------")  # Print a separator line for readability

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    view_database()  # Call the function to view the database content