import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from torch.cuda.amp import GradScaler, autocast
from model import get_banana_regression_model
from dataset import BananaRotDataset
import os

# 1. Configuration & Hyperparameters
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCH_SIZE = 16
EPOCHS = 30           # Increased because Early Stopping will handle the cutoff
LR_BACKBONE = 1e-5    # Slow learning for the ResNet layers
LR_HEAD = 1e-4        # Faster learning for our new regression head
PATIENCE = 4          # Stop if Val Loss doesn't improve for 4 epochs

# 2. Data Loading
full_dataset = BananaRotDataset(csv_file="banana_labels.csv", root_dir="./banana_dataset")
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_ds, val_ds = random_split(full_dataset, [train_size, val_size])

train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

# 3. Model Setup & Surgery
model = get_banana_regression_model()
# Unfreeze Layer 4 and the FC head for fine-tuning
for name, param in model.named_parameters():
    if "layer4" in name or "fc" in name:
        param.requires_grad = True
    else:
        param.requires_grad = False

model = model.to(device)

# 4. Optimizer, Scheduler, and Scaler
optimizer = torch.optim.Adam([
    {'params': model.layer4.parameters(), 'lr': LR_BACKBONE},
    {'params': model.fc.parameters(), 'lr': LR_HEAD}
])

# Automatically reduces LR when the model stops improving
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2)

# For 16-bit precision training (Faster on GPUs)
scaler = GradScaler()
criterion = nn.HuberLoss()

# 5. Training Loop with Early Stopping
best_val_loss = float('inf')
epochs_without_improvement = 0

print(f"🚀 Starting SOTA Training on {device}...")

for epoch in range(EPOCHS):
    # --- TRAINING PHASE ---
    model.train()
    train_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device).float().unsqueeze(1)
        
        optimizer.zero_grad()
        
        # Mixed Precision Forward Pass
        with autocast():
            outputs = model(images)
            loss = criterion(outputs, labels)
        
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        
        train_loss += loss.item()

    # --- VALIDATION PHASE ---
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device).float().unsqueeze(1)
            with autocast():
                outputs = model(images)
                val_loss += criterion(outputs, labels).item()

    avg_train_loss = train_loss / len(train_loader)
    avg_val_loss = val_loss / len(val_loader)
    
    print(f"Epoch {epoch+1:02d} | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")

    # 6. Step the Scheduler
    scheduler.step(avg_val_loss)

    # 7. Early Stopping & Best Model Checkpoint
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        torch.save(model.state_dict(), "banana_model_sota.pth")
        epochs_without_improvement = 0
        print("⭐ New Best Model Saved!")
    else:
        epochs_without_improvement += 1
        if epochs_without_improvement >= PATIENCE:
            print(f"🛑 Early stopping triggered. Model converged at epoch {epoch+1}.")
            break

print(f"✅ Final Training Complete. Best Val Loss: {best_val_loss:.4f}")