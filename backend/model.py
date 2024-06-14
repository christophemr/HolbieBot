import torch
import torch.nn as nn

class NeuralNet(nn.Module):
    """
    A simple neural network class for classification tasks.

    Attributes:
        l1 (nn.Linear): The first linear layer.
        l2 (nn.Linear): The second linear layer.
        l3 (nn.Linear): The third linear layer.
        relu (nn.ReLU): The ReLU activation function.

    Methods:
        forward(x): Defines the forward pass of the network.
    """

    def __init__(self, input_size, hidden_size, num_classes):
        """
        Initializes the NeuralNet class with given parameters.

        Args:
            input_size (int): The size of the input layer.
            hidden_size (int): The size of the hidden layers.
            num_classes (int): The number of output classes.

        Returns:
            None
        """
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        """
        Defines the forward pass of the network.

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            torch.Tensor: The output tensor after passing through the network.
        """
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out