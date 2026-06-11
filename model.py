import torch
import torch.nn as nn
from torchvision import models

def get_banana_regression_model():
    """
    Loads a pre-trained ResNet18 and modifies the final layer 
    to output a single number (Days to Death).
    """
    # 1. Load the weights from a model trained on millions of images
    # This gives your model "vision" out of the box.
    model = models.resnet18(weights='DEFAULT')

    # 2. Freeze the 'Backbone'
    # We don't want to change the layers that recognize shapes/colors.
    # We only want to train the new 'decision' layer at the end.
    for param in model.parameters():
        param.requires_grad = False

    # 3. Perform 'Surgery' on the Fully Connected (fc) layer
    # ResNet18 normally outputs 1000 categories. 
    # We change it to 1 for Regression (a single float value).
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, 1) 
    
    # 4. Make sure the new layer is trainable
    for param in model.fc.parameters():
        param.requires_grad = True

    return model

if __name__ == "__main__":
    # Quick test to see if the model initializes correctly
    test_model = get_banana_regression_model()
    print("✅ ResNet18 Surgery Successful!")
    print(f"Final Layer Structure: {test_model.fc}")
    
    # Dummy pass: Check if it can process a single blank image
    dummy_input = torch.randn(1, 3, 224, 224)
    output = test_model(dummy_input)
    print(f"Test Prediction Shape: {output.shape}") # Should be [1, 1]