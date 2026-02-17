# Enhancing Face Anti-Spoofing Using Transformer Networks

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![PyTorch](https://img.shields.io/badge/pytorch-2.2+-ee4c2c.svg)
![Flask](https://img.shields.io/badge/flask-v3.0-lightgrey.svg)

This repository implements an advanced **Face Anti-Spoofing (FAS)** framework. By combining **Vision Transformers (ViT)** with a **Selective Patch Attention Network (SPAN)** and **Multi-Scale Weighted Fusion (MSWF)**, the system identifies sophisticated presentation attacks (print, replay, 3D masks) with high precision.

---

## 🏗 System Architecture

The project moves away from standard CNNs to leverage the global context of Transformers. 

* **ViT Backbone:** Uses `vit_base_patch16_224` to process images as sequences of patches.
* **SPAN (Selective Patch Attention Network):** Implements **Contextual Reasoning Attention (CRA)** to calculate patch importance scores, focusing on regions with subtle spoofing artifacts.
* **MSWF (Multi-Scale Weighted Fusion):** Employs **Complementary Hierarchical Fusion** to merge high-level and low-level features, ensuring robustness against varying resolutions.



---

## 📊 Performance
The model was trained and validated on the **SiW (Spoof in the Wild)** dataset.

| Metric | SiW Development | SiW Evaluation |
| :--- | :--- | :--- |
| **APCER** | 0.0000 | 0.0000 |
| **BPCER** | 0.0918 | 0.0240 |
| **ACER** | 0.0459 | **0.0120** |
| **Accuracy** | 99.4% | **95.6%** |

---

## 📂 Project Structure

```text
├── app/
│   ├── static/          # CSS and Client-side assets
│   ├── templates/       # Flask HTML templates (index.html, result.html)
│   └── app.py           # Flask Web Framework entry point
├── models/
│   ├── vit_span.py      # Core ViT + SPAN + MSWF implementation
│   └── layers.py        # CRA and Multi-scale fusion modules
├── checkpoints/
│   └── justsiw.pth      # Pre-trained model weights
├── notebooks/
│   └── SPAN+MSWF_SIW.ipynb  # Training and Evaluation pipeline
└── requirements.txt     # Dependency list
```
---
## 🌐 Web Application (Flask)
The project includes a real-time web interface for testing face anti-spoofing measures.

Image Upload: Users can upload or capture a face image via the browser.

Processing: The Flask backend preprocesses the image (Resize to 224x224, Normalization).

Inference: The FaceSpoofDetector returns a probability score.

Result: The UI displays whether the input is "Real" or "Spoof" along with the confidence interval.

### Running the App
```bash
cd app
python app.py
```

## 🛠 Installation
Use the following command to install the required dependencies:

``` bash
pip install torch torchvision timm flask transformers
```

Then navigate to http://127.0.0.1:5000 in your browser.




