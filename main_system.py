import banana_engine # This is YOUR C++ code!

# Let's pretend our AI predicted a very old banana
banana_id = 101
predicted_age = 7.5

# Call the C++ Brain directly
result = banana_engine.get_best_route(banana_id, predicted_age)

print(f"--- Banana Logistics System ---")
print(f"Banana ID: {banana_id}")
print(f"AI Prediction: {predicted_age} days")
print(f"C++ Decision: {result}")