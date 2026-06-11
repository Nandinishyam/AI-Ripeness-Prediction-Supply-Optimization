import json
import random

def create_mock_data():
    # 1. Define where the Grocery Stores are (X, Y coordinates)
    stores = [
        {"id": "Store_A", "location": [10, 80]},
        {"id": "Store_B", "location": [90, 20]},
        {"id": "Store_C", "location": [50, 50]}
    ]

    # 2. Simulate 100 Bananas sitting in the warehouse
    inventory = []
    for i in range(100):
        banana = {
            "id": i,
            # Each banana gets a random "Age" (1.0 to 8.0) 
            # This mimics your AI's prediction
            "age": round(random.uniform(1.0, 8.0), 2),
            # Where the banana is sitting on the warehouse floor
            "shelf_pos": [random.randint(0, 20), random.randint(0, 20)]
        }
        inventory.append(banana)

    # 3. Save this to a JSON file so C++ can read it later
    data = {
        "warehouse_location": [0, 0],
        "stores": stores,
        "inventory": inventory
    }

    with open("warehouse_data.json", "w") as f:
        json.dump(data, f, indent=4)
    
    print("✅ Success! 'warehouse_data.json' created with 100 bananas.")

if __name__ == "__main__":
    create_mock_data()