import unittest
import torch
from model import NeuralNet

class TestModel(unittest.TestCase):

    def test_neural_net(self):
        input_size = 10
        hidden_size = 5
        output_size = 2
        model = NeuralNet(input_size, hidden_size, output_size)
        self.assertIsInstance(model, NeuralNet)
        sample_input = torch.randn(1, input_size)
        output = model(sample_input)
        self.assertEqual(output.shape, (1, output_size))

if __name__ == "__main__":
    unittest.main()
