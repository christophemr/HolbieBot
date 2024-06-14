import random
import json
import torch
import sqlite3
from datetime import datetime
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the French model
with open('intents_fr.json', 'r', encoding='utf-8') as f:
    intents_fr = json.load(f)

FILE_FR = 'données.pth'
data_fr = torch.load(FILE_FR)
input_size_fr = data_fr["input_size"]
hidden_size_fr = data_fr["hidden_size"]
output_size_fr = data_fr["output_size"]
all_words_fr = data_fr["all_words"]
tags_fr = data_fr["tags"]
model_state_fr = data_fr["model_state"]
model_fr = NeuralNet(input_size_fr, hidden_size_fr, output_size_fr).to(device)
model_fr.load_state_dict(model_state_fr)
model_fr.eval()

# Load the English model
with open('intents_en.json', 'r', encoding='utf-8') as f:
    intents_en = json.load(f)

FILE_EN = 'données_en.pth'
data_en = torch.load(FILE_EN)
input_size_en = data_en["input_size"]
hidden_size_en = data_en["hidden_size"]
output_size_en = data_en["output_size"]
all_words_en = data_en["all_words"]
tags_en = data_en["tags"]
model_state_en = data_en["model_state"]
model_en = NeuralNet(input_size_en, hidden_size_en, output_size_en).to(device)
model_en.load_state_dict(model_state_en)
model_en.eval()

# Generate Holberton keywords from tags
holberton_keywords = tags_fr + tags_en

def log_question(question, response, language, tag, confidence, is_out_of_scope):
    """
    Log the user's question and the chatbot's response to the database.

    Args:
        question (str): The user's question.
        response (str): The chatbot's response.
        language (str): The language of the conversation ('fr' or 'en').
        tag (str): The intent tag of the question.
        confidence (float): The confidence score of the predicted tag.
        is_out_of_scope (bool): Whether the question is out of scope for the chatbot.
    """
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO questions (question, response, language, timestamp, tag, confidence, is_out_of_scope)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (question, response, language, datetime.now(), tag, confidence, is_out_of_scope))
    conn.commit()
    conn.close()

def get_response_fr(message):
    """
    Get the chatbot's response for a French message.

    Args:
        message (str): The user's message.

    Returns:
        str: The chatbot's response.
    """
    return get_response(message, model_fr, all_words_fr, tags_fr, intents_fr, 'fr')

def get_response_en(message):
    """
    Get the chatbot's response for an English message.

    Args:
        message (str): The user's message.

    Returns:
        str: The chatbot's response.
    """
    return get_response(message, model_en, all_words_en, tags_en, intents_en, 'en')

def get_response(message, model, all_words, tags, intents, language):
    """
    Generate a response from the chatbot based on the user's message.

    Args:
        message (str): The user's message.
        model (NeuralNet): The language model to use.
        all_words (list): List of all words the model knows.
        tags (list): List of intent tags.
        intents (dict): Dictionary of intents and responses.
        language (str): The language of the conversation ('fr' or 'en').

    Returns:
        str: The chatbot's response.
    """
    sentence = tokenize(message)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                response = random.choice(intent["responses"])
                log_question(message, response, language, tag, prob.item(), False)
                return response
    else:
        # Check if the message is out of scope
        if not any(keyword in message.lower() for keyword in holberton_keywords):
            response = "Je suis programmé pour répondre aux questions concernant Holbertonschool. Pouvez-vous reformuler votre question à ce sujet?" if language == 'fr' else "I am programmed to answer questions about Holbertonschool. Could you please rephrase your question related to it?"
            log_question(message, response, language, "out_of_scope", prob.item(), True)
            return response

        response = "Je n'ai pas compris..." if language == 'fr' else "I didn't understand..."
        log_question(message, response, language, "unknown", prob.item(), False)
        return response

# Main loop for the chatbot interaction in cli
if __name__ == "__main__":
    """
    Main loop to run the chatbot interaction in the console.

    This loop will continue to prompt the user for input until 'quit' is entered.
    The default language for testing is set to French.
    """
    print("Chatbot is running! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        response = get_response_fr(user_input)  # Defaulting to French for testing
        print(f"Chatbot: {response}")