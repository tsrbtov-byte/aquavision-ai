import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torchvision.models import efficientnet_b2, EfficientNet_B2_Weights
import os

def main():
    print("🚀 AquaVision AI — EfficientNet-B2 Model Təlimi Başlayır...")
    
    # 1. Gücləndirilmiş Data Augmentation
    data_transforms = {
        'clean': transforms.Compose([
            transforms.Resize((260, 260)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomRotation(25),
            transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    }

    data_dir = 'dataset'
    if not os.path.exists(data_dir):
        print("❌ 'dataset' qovluğu tapılmadı! Lütfən dataset/clean və dataset/polluted qovluqlarını yaradın.")
        return

    image_dataset = datasets.ImageFolder(data_dir, data_transforms['clean'])
    dataloader = torch.utils.data.DataLoader(image_dataset, batch_size=16, shuffle=True, num_workers=0)

    print(f"📦 Ümumi Təlim Şəkillərinin Sayı: {len(image_dataset)}")
    print(f"🏷️ Siniflər: {image_dataset.classes}")

    # 2. EfficientNet-B2 Arxitekturası
    weights = EfficientNet_B2_Weights.DEFAULT
    model = efficientnet_b2(weights=weights)

    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_ftrs, 2)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"⚡ Təlim Cihazı: {device}")
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.0003, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)

    # 3. Model Təlim Dövrü (Epochs = 15)
    epochs = 15
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        running_corrects = 0

        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

        scheduler.step()

        epoch_loss = running_loss / len(image_dataset)
        epoch_acc = running_corrects.double() / len(image_dataset)

        print(f"Epoch {epoch+1}/{epochs} - İtki (Loss): {epoch_loss:.4f} - Dəqiqlik (Accuracy): {epoch_acc*100:.2f}%")

    # 4. Modeli Yadda Saxlamaq
    torch.save(model.state_dict(), "water_model.pth")
    print("✅ Model uğurla 'water_model.pth' faylına yazıldı! İndi Streamlit tətbiqini başladın.")

if __name__ == '__main__':
    main()
