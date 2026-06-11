import os
import pandas as pd

# This points to the folder you just dropped into VS Code
DATASET_DIR = "./banana_dataset" 

def generate_csv_labels(data_dir):
    print("Initializing high-speed data extraction...")
    data = []
    
    # os.walk rapidly scans through all sub-folders automatically
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Filename example: honey_banana_1_4.jpg
                try:
                    # We split the text by '_' to isolate the '4.jpg', then split by '.' to get '4'
                    day_str = file.split('_')[-1].split('.')[0]
                    actual_days = float(day_str)
                    
                    # Store the exact path so the neural network can find it later
                    rel_path = os.path.relpath(os.path.join(root, file), data_dir)
                    data.append({"image_path": rel_path, "days_to_death": actual_days})
                except Exception:
                    # If a random file doesn't match the format, skip it cleanly without crashing
                    continue

    if not data:
        print("ERROR: No images found. Check if your folder is named exactly 'banana_dataset'.")
        return

    # Convert to a highly optimized Pandas DataFrame and save to disk
    df = pd.DataFrame(data)
    df.to_csv("banana_labels.csv", index=False)
    print(f"SUCCESS! Extracted labels for {len(df)} images. Saved to banana_labels.csv")

if __name__ == "__main__":
    # Inside dataset.py -> __init__
   
    generate_csv_labels(DATASET_DIR)