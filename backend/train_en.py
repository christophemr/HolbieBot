import json
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet
import multiprocessing


if __name__ == '__main__':
    """
    Main function to train the chatbot model with given intents data.

    Steps:
    1. Load intents data from 'intents_en.json'.
    2. Tokenize and stem the words from patterns, and create a vocabulary.
    3. Create training data (bag-of-words) for the patterns and their corresponding tags.
    4. Define a custom dataset class `ChatDataset` for loading training data.
    5. Initialize the neural network model, loss function, and optimizer.
    6. Train the model using the DataLoader for a specified number of epochs.
    7. Save the trained model and other related data to a file.

    The model is trained using PyTorch and saved for later use in the chatbot application.
    """
    # Load the intents file
    with open('intents_en.json', 'r', encoding='utf-8') as f:
        data = f.read()
        intents = json.loads(data)
    
    # Initialize lists to store all words, tags, and pattern-tag pairs
    all_words = []
    tags = []
    xy = []
    # process each intent in the intent file
    for intent in intents['intents']:
        tag = intent['tag']
        tags.append(tag)
        for pattern in intent['patterns']:
            w = tokenize(pattern)
            all_words.extend(w)
            xy.append((w, tag))
    
    # Remove special characters and stem all words
    ignore_words = ['?', '!', '.', ',']
    # Stem and sort all words, removing duplicates
    all_words = [stem(w) for w in all_words if w not in ignore_words]
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))
    
    # Create training data
    x_train = []
    y_train = []
    for (pattern_sentence, tag) in xy:
        bag = bag_of_words(pattern_sentence, all_words)
        x_train.append(bag)
        
        label = tags.index(tag)
        y_train.append(label) # CrossEntropyLoss expects integer labels
    
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    
    class ChatDataset(Dataset):
        """
        Custom Dataset class for loading chat data.

        Attributes:
            n_samples (int): Number of samples in the dataset.
            x_data (np.ndarray): Input features.
            y_data (np.ndarray): Labels corresponding to input features.
        """
        def __init__(self):
            """
            Initializes the dataset with training data.
            """
            self.n_samples = len(x_train)
            self.x_data = x_train
            self.y_data = y_train
            
        def __getitem__(self, index):
            """
            Retrieves the sample and label at the specified index.

            Args:
                index (int): Index of the sample to retrieve.

            Returns:
                tuple: (sample, label) where sample is the input feature and label is the corresponding tag.
            """
            return self.x_data[index], self.y_data[index]
        
        def __len__(self):
            """
            Returns the number of samples in the dataset.

            Returns:
                int: Number of samples in the dataset.
            """
            return self.n_samples
    
    # Set Hyperparameters
    batch_size = 8
    hidden_size = 8
    output_size = len(tags)
    input_size = len(x_train[0])
    learning_rate = 0.001
    num_epochs = 400
    
    # Create dataset and dataloader
    dataset = ChatDataset()
    train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # initialize the neral network
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    # Training loop
    for epoch in range(num_epochs):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(device)
            
            # Convert labels to the correct data type (torch.long)
            labels = labels.long()
            
            # Forward pass
            outputs = model(words)
            loss = criterion(outputs, labels)
            
            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
        if (epoch + 1) % 100 == 0:
            print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')
    
    print(f'final loss, loss={loss.item():.4f}')

    # Save the trained model
    data = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "output_size": output_size,
        "hidden_size": hidden_size,
        "all_words": all_words,
        "tags": tags
    }

    FILE = 'données_en.pth'
    torch.save(data, FILE)
    
    print(f'training complete. file saved to {FILE}')
