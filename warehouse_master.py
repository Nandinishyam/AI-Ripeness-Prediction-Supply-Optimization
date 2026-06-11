import banana_engine  # Your C++ Module
import random
import time

def simulate_ai_camera():
    """Simulates the AI detecting a banana and predicting its age."""
    banana_id = random.randint(1000, 9999)
    # AI predicts age between 1.0 and 8.0 days
    predicted_age = round(random.uniform(1.0, 8.0), 1)
    return banana_id, predicted_age

print("--- 🍌 SMART WAREHOUSE REAL-TIME LOGISTICS ---")
print("Status: C++ Engine Linked | AI Model Loaded")
print("-" * 45)

try:
    for i in range(1, 6):
        # 1. AI "Sees" a banana
        bid, age = simulate_ai_camera()
        print(f"[SCAN {i}] Detected Banana #{bid} | Predicted Age: {age} days")

        # 2. C++ "Decides" the route instantly
        # This call goes straight into your compiled C++ memory!
        decision = banana_engine.get_best_route(bid, age)
        
        print(f" > ACTION: {decision}")
        time.sleep(1) # Simulate processing time

except Exception as e:
    print(f"❌ Error in Handshake: {e}")

print("-" * 45)
print("Batch Processing Complete. System Standby.")