import unittest
from chat import get_response_fr, get_response_en

class TestChat(unittest.TestCase):
    def test_get_response_fr(self):
        response = get_response_fr("salut")
        self.assertIsNotNone(response)

    def test_get_response_en(self):
        response = get_response_en("hello")
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()
