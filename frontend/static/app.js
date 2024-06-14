/**
 * Chatbox class to handle the functionalities of a chat interface.
 * This includes initialization, message handling, speech recognition,
 * language change, dragging functionality, and message sending/receiving.
 */
// @ts-ignore
class Chatbox {
  constructor() {
    // Initialize the elements and states needed for the chatbox functionality
    this.args = {
      openButton: document.querySelector('.chatbox__button'), // Button to open the chatbox
      chatBox: document.querySelector('.chatbox__support'), // Chatbox container
      sendButton: document.querySelector('.send__button'), // Button to send messages
      languageSelector: document.querySelector('#language'), // Dropdown to select language
      voiceInputButton: document.querySelector('#voiceInputButton'), // Button for voice input
      chatInput: document.querySelector('#chatInput'), // Input field for chat messages
      headerTitle: document.querySelector('#headerTitle'), // Header title of the chatbox
      headerDescription: document.querySelector('#headerDescription'), // Header description of the chatbox
      languageOptions: document.querySelector('.language-options') // Language options container
    };
    this.state = false; // State to check if chatbox is open or closed
    this.messages = []; // Array to store messages
    this.language = 'fr'; // Default language
    this.isVoiceInput = false; // State to check if voice input is active
    this.isFirstOpen = true; // State to check if chatbox is opened for the first time
    this.initRecognition(); // Initialize speech recognition
    this.initLanguageChange(); // Initialize language change functionality
    this.initDrag(); // Initialize drag functionality for the chatbox
  }

  // Method to enable dragging of the chatbox
  initDrag() {
    const chatBox = this.args.chatBox;
    if (!chatBox) {
      console.error('chatBox element is missing.');
      return;
    }

    const header = chatBox.querySelector('.chatbox__header');
    if (!header) {
      console.error('header element is missing.');
      return;
    }

    let offsetX, offsetY, isDragging = false;

    // Event listener to start dragging
    header.addEventListener('mousedown', (e) => {
      if (!(e instanceof MouseEvent)) return;
      if (!(chatBox instanceof HTMLElement) || !(header instanceof HTMLElement)) return;
      isDragging = true;
      offsetX = e.clientX - (chatBox.offsetLeft || 0);
      offsetY = e.clientY - (chatBox.offsetTop || 0);
      header.style.cursor = 'grabbing';
    });

    // Event listener to update chatbox position while dragging
    document.addEventListener('mousemove', (e) => {
      if (!(e instanceof MouseEvent) || !isDragging) return;
      if (chatBox instanceof HTMLElement) {
        chatBox.style.left = `${e.clientX - offsetX}px`;
        chatBox.style.top = `${e.clientY - offsetY}px`;
      }
    });

    // Event listener to stop dragging
    document.addEventListener('mouseup', () => {
      isDragging = false;
      if (header instanceof HTMLElement) {
        header.style.cursor = 'grab';
      }
    });
  }

  // Method to initialize speech recognition
  initRecognition() {
    // @ts-ignore
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.lang = this.language === 'fr' ? 'fr-FR' : 'en-US';
      this.recognition.interimResults = false;
      this.recognition.maxAlternatives = 1;

      // Event listener for speech result
      this.recognition.addEventListener('result', (event) => {
        const transcript = event.results[0][0].transcript.trim();
        const inputField = this.args.chatInput;
        if (inputField instanceof HTMLInputElement) {
          inputField.value = transcript;
          this.isVoiceInput = true;
          this.onSendButton(this.args.chatBox);
        }
      });

      // Event listener for speech end
      this.recognition.addEventListener('speechend', () => {
        this.recognition.stop();
      });

      // Event listener for speech recognition error
      this.recognition.addEventListener('error', (event) => {
        console.error('Speech recognition error detected: ' + event.error);
      });
    } else {
      console.error('SpeechRecognition API not supported in this browser.');
    }
  }

    // Method to display the chatbox and handle button interactions
    display() {
      const { openButton, chatBox, sendButton, languageSelector, voiceInputButton } = this.args;
  
      // Event listener to open the chatbox
      if (openButton) {
        openButton.addEventListener('click', () => {
          this.toggleState(chatBox);
          if (this.isFirstOpen) {
            this.sendWelcomeMessage(chatBox);
            this.isFirstOpen = false;
          }
        });
      }
  
      // Event listener to send a message
      if (sendButton) {
        sendButton.addEventListener('click', () => {
          this.isVoiceInput = false;
          this.onSendButton(chatBox);
        });
      }
  
      // Event listener to change language
      if (languageSelector && languageSelector instanceof HTMLSelectElement) {
        languageSelector.addEventListener('change', (event) => {
          const target = event.target;
          if (target && target instanceof HTMLSelectElement) {
            this.language = target.value;
            this.updateTextContent();
            if (this.recognition) {
              this.recognition.lang = this.language === 'fr' ? 'fr-FR' : 'en-US';
            }
          }
        });
      }
  
      // Event listener for voice input button
      if (voiceInputButton) {
        voiceInputButton.addEventListener('click', () => {
          if (this.recognition) {
            this.recognition.start();
          }
        });
      }
  
      // Event listener to send message on Enter key press
      const node = this.args.chatInput;
      if (node && node instanceof HTMLInputElement) {
        node.addEventListener('keyup', (event) => {
          if (event.key === 'Enter') {
            this.isVoiceInput = false;
            this.onSendButton(chatBox);
          }
        });
      }
    }
  
    // Method to send a welcome message when the chatbox is first opened
    sendWelcomeMessage(chatbox) {
      const welcomeMsg = {
        name: 'Betty',
        message: 'Bonjour! Veuillez choisir votre langue:\nHello! Please choose your language:',
        type: 'welcome'
      };
      this.addMessage(chatbox, welcomeMsg);
  
      const languageOptions = document.getElementById('languageOptions');
      if (languageOptions) {
        languageOptions.style.display = 'flex';
      }
    }
  
    // Method to initialize language change functionality
    initLanguageChange() {
      const languageSelector = this.args.languageSelector;
      if (languageSelector && languageSelector instanceof HTMLSelectElement) {
        languageSelector.addEventListener('change', () => {
          this.language = languageSelector.value;
          this.updateTextContent();
        });
      }
  
      // Event listeners for language change options
      const frenchOption = document.getElementById('frenchOption');
      const englishOption = document.getElementById('englishOption');
  
      if (frenchOption) {
        frenchOption.addEventListener('click', () => {
          this.language = 'fr';
          this.updateTextContent();
        });
      }
  
      if (englishOption) {
        englishOption.addEventListener('click', () => {
          this.language = 'en';
          this.updateTextContent();
        });
      }
    }
  
    // Method to update text content based on selected language
    updateTextContent() {
      const { sendButton, headerTitle, headerDescription, chatInput, voiceInputButton } = this.args;
      if (sendButton) {
        sendButton.textContent = this.language === 'fr' ? 'Envoyer' : 'Send';
      }
      if (headerTitle) {
        headerTitle.textContent = this.language === 'fr' ? 'Assistant Virtuel Betty' : 'Virtual Assistant Betty';
      }
      if (headerDescription) {
        headerDescription.textContent = this.language === 'fr' ? 'Bonjour. Posez-moi vos questions sur Holbertonschool' : 'Hello. Ask me your questions about Holbertonschool';
      }
      if (chatInput && chatInput instanceof HTMLInputElement) {
        chatInput.placeholder = this.language === 'fr' ? 'Écrivez un message...' : 'Write a message...';
      }
      if (voiceInputButton) {
        voiceInputButton.textContent = this.language === 'fr' ? '🎤' : '🎤';
      }
    }
      // Method to toggle the state of the chatbox
  toggleState(chatbox) {
    this.state = !this.state;
    if (chatbox) {
      chatbox.classList.toggle('chatbox--active', this.state);
    }
  }

  // Method to handle sending a message
  onSendButton(chatbox) {
    const textField = this.args.chatInput;
    if (!(textField instanceof HTMLInputElement)) {
      console.error('Text field element is missing.');
      return;
    }

    const text = textField.value.trim();
    if (text === '') {
      return;
    }

    const userMsg = { name: 'User', message: text };
    this.messages.push(userMsg);
    this.addMessage(chatbox, userMsg);

    console.log(`Sending message: ${text} in language: ${this.language}`);
    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      body: JSON.stringify({ message: text, language: this.language }),
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      },
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      const BettyMsg = { name: 'Betty', message: data.answer };
      this.showTypingIndicator(chatbox);

      setTimeout(() => {
        this.hideTypingIndicator(chatbox);
        this.addMessageCharacterByCharacter(chatbox, BettyMsg);
        this.scrollToBottom(chatbox ? chatbox.querySelector('.chatbox__messages') : null);
        if (this.isVoiceInput) {
          this.speak(BettyMsg.message);
        }
      }, 2000); // Délai pour simuler la frappe
    })
    .catch(error => {
      console.error('Error:', error);
    });

    textField.value = '';
  }

  // Method to add a message to the chatbox
  addMessage(chatbox, message) {
    const chatmessage = chatbox ? chatbox.querySelector('.chatbox__messages') : null;
    if (!chatmessage) {
      console.error('Chat messages container is missing.');
      return;
    }

    const className = message.name === 'Betty' ? 'messages__item--visitor' : 'messages__item--operator';
    const messageElement = document.createElement('div');
    messageElement.className = `messages__item ${className}`;
    messageElement.textContent = message.message;
    chatmessage.appendChild(messageElement);
    this.scrollToBottom(chatmessage);

    if (message.name === 'Betty' && message.type === 'welcome') {
      // Increase size of language flags in the message
      const flags = messageElement.querySelectorAll('img');
      flags.forEach(flag => {
        flag.style.width = '40px';
        flag.style.height = '30px';
      });
    }
  }

  // Method to add a message character by character (typing effect)
  addMessageCharacterByCharacter(chatbox, message) {
    const chatmessage = chatbox ? chatbox.querySelector('.chatbox__messages') : null;
    if (!chatmessage) {
      console.error('Chat messages container is missing.');
      return;
    }

    const className = message.name === 'Betty' ? 'messages__item--visitor' : 'messages__item--operator';
    const messageElement = document.createElement('div');
    messageElement.className = `messages__item ${className}`;
    chatmessage.appendChild(messageElement);

    let index = 0;
    const typingSpeed = 25;

    const typeInterval = setInterval(() => {
      if (index < message.message.length) {
        messageElement.textContent += message.message.charAt(index);
        index++;
        this.scrollToBottom(chatmessage);
      } else {
        clearInterval(typeInterval);
      }
    }, typingSpeed);
  }

  // Method to show typing indicator
  showTypingIndicator(chatbox) {
    const typingIndicator = chatbox ? chatbox.querySelector('#typingIndicator') : null;
    if (typingIndicator) {
      typingIndicator.style.display = 'flex';
    }
  }

  // Method to hide typing indicator
  hideTypingIndicator(chatbox) {
    const typingIndicator = chatbox ? chatbox.querySelector('#typingIndicator') : null;
    if (typingIndicator) {
      typingIndicator.style.display = 'none';
    }
  }

  // Method to scroll chat to the bottom
  scrollToBottom(chatmessage) {
    if (chatmessage) {
      chatmessage.scrollTop = chatmessage.scrollHeight;
    } else {
      console.error('Chat messages container is missing.');
    }
  }

  // Method to synthesize speech for a given message
  speak(message) {
    console.log(`Synthesizing speech for: ${message}`);
    const speechSynthesis = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(message);
    utterance.lang = this.language === 'fr' ? 'fr-FR' : 'en-US';

    // Adjusting the speech rate based on the language
    if (utterance.lang === 'fr-FR') {
      utterance.rate = 2.5; // Set the rate for French
    } else {
      utterance.rate = 1; // Set the rate for English
    }

    speechSynthesis.speak(utterance);
  }
}

// @ts-ignore
const chatbox = new Chatbox();
chatbox.display();

