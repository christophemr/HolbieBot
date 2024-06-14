"""
This module provides utility functions for natural language processing (NLP) tasks.
It includes functions to tokenize sentences, stem words, and create bag-of-words representations.
"""

# Uncomment the following line if you need to download the punkt tokenizer data
# nltk.download('punkt')


import nltk
#nltk.download('punkt')
import numpy as np
from nltk.stem.porter import PorterStemmer

# Initialize the Porter stemmer
stemmer = PorterStemmer()

def tokenize(sentence):
    """
    Tokenize a sentence into words.
    
    Args:
        sentence (str): The sentence to tokenize.
    
    Returns:
        list: A list of words (tokens) from the sentence.
    """
    return nltk.word_tokenize(sentence)

def stem(word):
    """
    Stem a word to its root form.
    
    Args:
        word (str): The word to stem.
    
    Returns:
        str: The stemmed word in lowercase.
    """
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    """
    Create a bag-of-words representation of the sentence.
    
    Args:
        tokenized_sentence (list): A list of words from the tokenized sentence.
        all_words (list): A list of all words used for the bag-of-words model.
    
    Returns:
        numpy.ndarray: A bag-of-words array where each index represents the presence of a word in the sentence.
    """
    # Stem each word in the tokenized sentence
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    
    # Initialize the bag of words vector with zeros
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0

    return bag
