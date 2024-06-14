import unittest
from nltk_utils import tokenize, stem, bag_of_words

class TestNltkUtils(unittest.TestCase):

    def test_tokenize(self):
        sentence = "Hello, how are you?"
        tokens = tokenize(sentence)
        self.assertEqual(tokens, ["Hello", ",", "how", "are", "you", "?"])

    def test_stem(self):
        word = "running"
        stemmed_word = stem(word)
        self.assertEqual(stemmed_word, "run")

    def test_bag_of_words(self):
        tokenized_sentence = ["hello", "world"]
        all_words = ["hi", "hello", "world", "python"]
        bag = bag_of_words(tokenized_sentence, all_words)
        self.assertEqual(bag.tolist(), [0, 1, 1, 0])

if __name__ == "__main__":
    unittest.main()
