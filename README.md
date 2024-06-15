# HolbieBot

HolbieBot is an AI-powered chatbot designed to assist users with queries related to Holberton School. It supports multiple languages and integrates speech recognition for seamless interaction. The project utilizes various machine learning libraries and frameworks to provide accurate and efficient responses.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Features

- Supports multiple languages (French and English)
- Speech recognition capabilities
- Responsive design for mobile and desktop views
- Stores and logs user interactions
- Easy to extend and modify

## Project Structure

The project is organized as follows:
```
HolbieBot/
├── backend/
│   ├── database/
│   │   ├── init_db.py
│   │   ├── view_db.py
│   ├── intents/
│   │   ├── intents_fr.json
│   │   ├── intents_en.json
│   ├── __init__.py
│   ├── app.py
│   ├── chat.py
│   ├── model.py
│   ├── nltk_utils.py
│   ├── train_fr.py
│   ├── train_en.py
│   ├── tests/
│   │   ├── test_app.py
│   │   ├── test_chat.py
│   │   ├── test_init_db.py
│   │   ├── test_view_db.py
│   │   ├── test_train_en.py
│   │   ├── test_train_fr.py
├── frontend/
│   ├── static/
│   │   ├── images/
│   │   │   ├── logo.png
│   │   │   ├── french-flag.png
│   │   │   ├── english-flag.png
│   │   ├── app.js
│   │   ├── style.css
├── README.md
├── .gitignore
├── .env
```



## Installation

To get started with HolbieBot, follow these steps:

### Prerequisites

- Python 3.8+
- Flask
- PyTorch
- NLTK

### Backend Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/christophemr/HolbieBot.git
    cd HolbieBot/backend
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python -m venv .env
    source .env/bin/activate  # On Windows use `.env\Scripts\activate`
    ```

3. **Install the required Python packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    ```sh
    python database/init_db.py
    ```

5. **Run the training scripts**:
    ```sh
    python train_en.py
    python train_fr.py
    ```

6. **Start the Flask app**:
    ```sh
    python app.py
    ```

## Usage

Once the backend server is running, open your web browser and go to `http://127.0.0.1:5000` to interact with HolbieBot.

## Running Tests

To run the tests, use the following command in the `backend` directory:

```sh
python -m unittest discover -s tests
```

## Updating the Intents File

To train the chatbot for different purposes, you need to update the intents.json file with your own data. The intents.json file contains training data in the form of intents, patterns, and responses. Each intent represents a category of user input and includes examples of what users might say and the corresponding responses.
```
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": ["Hi", "Hello", "How are you?", "Good morning"],
      "responses": ["Hello!", "Hi there!", "Greetings!"],
      "context_set": ""
    },
    {
      "tag": "goodbye",
      "patterns": ["Bye", "See you later", "Goodbye"],
      "responses": ["Goodbye!", "See you later!"],
      "context_set": ""
    }
  ]
}
```

tag: A label for the intent.
patterns: Example phrases that users might say to trigger this intent.
responses: The chatbot's responses for the intent.
context_set: (Optional) Context information to handle specific conversation flows.

### Steps to Update the Intents File

1. Open the intents.json file: You can find this file in the backend directory of the project.

2. Modify or add new intents: Follow the structure shown above to add your own intents, patterns, and responses. (Don't forget that there are 2 intent.json files, 1 for each language) 

3. Save the file: Ensure the JSON structure is correctly formatted.

### Re-train the Model

After updating the intents.json file, you need to re-train the model to learn from the new data:
```sh
python backend/train.py
```

This will generate a new model file (données.pth) that the chatbot will use to understand and respond to user inputs based on the updated intents


## Contributing

Contributions are welcome! Please fork this repository and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to Holberton School for the inspiration and resources provided to make this project possible.
