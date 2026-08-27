# 🌊 AquaVision AI — Digital Water Quality Analysis

AquaVision AI is a lightweight computer vision system designed for early detection of visual water contamination using deep learning. Powered by PyTorch, MobileNetV2, and OpenCV, it analyzes water sample images to instantly flag potential pollution hazards.

## 🚀 Key Features
* **Transfer Learning Architecture:** Built on MobileNetV2 fine-tuned for high-accuracy binary classification (Clean vs. Polluted).
* **Dual Input Modes:** Supports single-image file uploads (`.jpg`, `.png`, `.webp`) and real-time webcam captures.
* **Interactive Dashboard:** Deployed using Streamlit for instant predictions and confidence scoring.

## 🛠️ Project Structure
```text
SA 2026/
├── dataset/             # Sample images (clean/polluted)
├── app.py               # Streamlit application entry point
├── train.py             # PyTorch training script
├── water_model.pth      # Fine-tuned MobileNetV2 weights
└── requirements.txt     # Environment dependencies