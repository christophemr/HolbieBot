import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_predict(self):
        response = self.app.post('/predict', json={"message": "hello", "language": "en"})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
