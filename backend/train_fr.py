import json
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet
import multiprocessing

# Main function to train the chatbot model
if __name__ == '__main__':
    # Load intents from JSON file
    with open('intents_fr.json','r', encoding='utf-8') as f:
        data = f.read()
        intents = json.loads(data)
        
    all_words = []
    tags = []
    xy = []

    # Process each intent in the JSON file
    for intent in intents['intents']:
        tag = intent['tag']
        tags.append(tag)  # Add tag to the list
        for pattern in intent['patterns']:
            w = tokenize(pattern)  # Tokenize each pattern
            all_words.extend(w)  # Add tokenized words to all_words
            xy.append((w, tag))  # Add tuple (tokenized pattern, tag) to xy
            
    ignore_words = ['?', '!', '.', ',']
    # Stem and lower the words, and remove ignore words
    all_words = [stem(w) for w in all_words if w not in ignore_words]
    # Sort and remove duplicates
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))
    
    x_train = []
    y_train = []

    # Create training data
    for (pattern_sentence, tag) in xy:
        bag = bag_of_words(pattern_sentence, all_words)  # Create bag of words vector
        x_train.append(bag)
        
        label = tags.index(tag)  # CrossEntropyLoss needs the target label as an integer
        y_train.append(label)  # Add label to y_train
        
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    
    class ChatDataset(Dataset):
        """Dataset class for loading the training data"""
        def __init__(self):
            """Initialize the dataset with x_train and y_train data"""
            self.n_samples = len(x_train)
            self.x_data = x_train
            self.y_data = y_train
            
        def __getitem__(self, index):
            """Return a sample from the dataset at the given index"""
            return self.x_data[index], self.y_data[index]
        
        def __len__(self):
            """Return the total number of samples in the dataset"""
            return self.n_samples
    
    batch_size = 8
    hidden_size = 8
    output_size = len(tags)
    input_size = len(x_train[0])
    learning_rate = 0.001
    num_epochs = 500
    
    dataset = ChatDataset()
    train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    
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
            
        if (epoch +1) % 100 == 0:
            print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')
    
    print(f'final loss, loss={loss.item():.4f}')

    # Save the trained model and metadata
    données = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "output_size": output_size,
        "hidden_size": hidden_size,
        "all_words": all_words,
        "tags": tags
    }

    FILE = 'données.pth'
    torch.save(données, FILE)
    
    print(f'training complete. file saved to {FILE}')