from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_response_fr, get_response_en

app = Flask(__name__, static_folder='../frontend/static', template_folder='templates')
CORS(app)

@app.get("/")
def index():
    """
    Render the main page of the chatbot interface.

    This route handles GET requests to the root URL ("/") and returns the index.html template.
    
    Returns:
        Response: Rendered HTML template for the main page.
    """
    return render_template('index.html')

@app.post("/predict")
def predict():
    """
    Handle the chatbot response generation.

    This route handles POST requests to the "/predict" URL. It retrieves the user's message
    and the selected language from the request JSON, processes the message through the appropriate
    language model, and returns the chatbot's response.

    Returns:
        Response: JSON response containing the chatbot's answer.
    """
    data = request.get_json()
    text = data.get("message")
    language = data.get("language")

    if language == "fr":
        response = get_response_fr(text)
    else:
        response = get_response_en(text)

    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)