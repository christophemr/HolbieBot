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

HolbieBot/
├── backend/
│ ├── database/
│ │ ├── init_db.py
│ │ ├── view_db.py
│ ├── intents/
│ │ ├── intents_fr.json
│ │ ├── intents_en.json
│ ├── tests/
│ │ ├── test_app.py
│ │ ├── test_chat.py
│ │ ├── test_init_db.py
│ │ ├── test_view_db.py
│ │ ├── test_train_en.py
│ │ ├── test_train_fr.py
│ ├── app.py
│ ├── chat.py
│ ├── model.py
│ ├── nltk_utils.py
│ ├── train_en.py
│ ├── train_fr.py
├── frontend/
│ ├── static/
│ │ ├── images/
│ │ │ ├── logo.png
│ │ │ ├── french-flag.png
│ │ │ ├── english-flag.png
│ │ ├── app.js
│ │ ├── style.css
├── .env
├── .gitignore
├── README.md


## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/christophemr/HolbieBot.git
cd HolbieBot

2. Set up the Python environment:
python -m venv .env
source .env/bin/activate  # On Windows, use `.env\Scripts\activate`
pip install -r requirements.txt

3. Initialize the database:
python backend/database/init_db.py

4. Train the models:
python backend/train_en.py
python backend/train_fr.py

## Usage

1. Start the Flask app:
python backend/app.py

2. Open your browser and navigate to http://127.0.0.1:5000 to interact with HolbieBot.

## Running Tests

To run the tests, use the following command:
python -m unittest discover backend/tests

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to Holberton School for the inspiration and resources provided to make this project possible.
