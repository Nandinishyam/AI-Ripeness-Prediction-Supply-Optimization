import torch
import torch.nn as nn
from PIL import Image
import os
from model import get_banana_regression_model # From your Day 2 file
from dataset import BananaRotDataset          # From your Day 1 file

# ==========================================
# 1. DYNAMIC CONFIGURATION
# ==========================================
# Point to your saved model and the folder containing test images
MODEL_PATH = "banana_model.pth"
TEST_FOLDER = r"C:\Users\Shyam Prasad\Desktop\Banana_Project\banana_dataset\test\honeybanana"

def predict_days():
    # A. Find an image automatically so we avoid FileNotFoundError
    all_files = [f for f in os.listdir(TEST_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not all_files:
        print(f"❌ Error: No images found in {TEST_FOLDER}")
        return

    # Let's pick the first image in the folder
    sample_image_name = all_files[0]
    image_path = os.path.join(TEST_FOLDER, sample_image_name)

    # ==========================================
    # 2. SETUP THE BRAIN
    # ==========================================
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load the architecture (Day 2)
    model = get_banana_regression_model()
    
    # Load the learned knowledge (Day 3)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval() # Set to evaluation mode

    # ==========================================
    # 3. PRE-PROCESS THE IMAGE
    # ==========================================
    # We use the exact same transform you defined in your dataset.py
    # Note: We create a dummy dataset object just to steal its 'transform' logic
    temp_ds = BananaRotDataset(csv_file="banana_labels.csv", root_dir="./banana_dataset")
    transform = temp_ds.transform

    # Load and transform the image
    img = Image.open(image_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(device) # unsqueeze(0) adds the 'batch' dimension

    # ==========================================
    # 4. RUN INFERENCE (THE PREDICTION)
    # ==========================================
    with torch.no_grad():
        output = model(img_tensor)
    
    predicted_val = output.item()

    # ==========================================
    # 5. OUTPUT RESULTS
    # ==========================================
    print("\n" + "="*40)
    print("🍌 BANANA RIPENESS INFERENCE REPORT")
    print("="*40)
    print(f"Testing Image : {sample_image_name}")
    print(f"Predicted Day : {predicted_val:.2f}")
    print("-" * 40)
    
    # Logic Check for User
    if predicted_val > 5:
        print("Status: OLD/ROTTEN (High Age)")
    else:
        print("Status: FRESH/YOUNG (Low Age)")
    print("="*40 + "\n")

if __name__ == "__main__":
    predict_days()