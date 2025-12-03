"""
Download required models for detection and segmentation.
"""
import os
import urllib.request
from pathlib import Path
from ultralytics import YOLO

# Create models directory
MODELS_DIR = Path("data/models")
MODELS_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("DOWNLOADING DETECTION AND SEGMENTATION MODELS")
print("=" * 60)

# 1. Download YOLO models
print("\n[1/3] Downloading YOLOv8 models...")
print("-" * 60)

yolo_models = [
    "yolov8n.pt",  # Nano - fastest
    "yolov8s.pt",  # Small
    "yolov8m.pt",  # Medium - good balance
]

for model_name in yolo_models:
    try:
        print(f"\nDownloading {model_name}...")
        # YOLO will auto-download if not present
        model = YOLO(model_name)
        print(f"✓ {model_name} ready")
    except Exception as e:
        print(f"✗ Error downloading {model_name}: {e}")

# 2. Download SAM models
print("\n[2/3] Downloading SAM (Segment Anything) models...")
print("-" * 60)

sam_models = {
    "sam_vit_b_01ec64.pth": "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth",
    # Uncomment if you want larger models:
    # "sam_vit_l_0b3195.pth": "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth",
    # "sam_vit_h_4b8939.pth": "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth",
}

for model_name, url in sam_models.items():
    model_path = MODELS_DIR / model_name
    if model_path.exists():
        print(f"✓ {model_name} already exists (skipping)")
    else:
        try:
            print(f"\nDownloading {model_name}...")
            print(f"URL: {url}")
            print("This may take a few minutes (~375 MB)...")
            
            def progress(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = min(100, (downloaded / total_size) * 100)
                bar_length = 40
                filled = int(bar_length * percent / 100)
                bar = '█' * filled + '░' * (bar_length - filled)
                print(f"\r[{bar}] {percent:.1f}% ({downloaded / 1024 / 1024:.1f} MB)", end='')
            
            urllib.request.urlretrieve(url, model_path, reporthook=progress)
            print(f"\n✓ {model_name} downloaded successfully")
        except Exception as e:
            print(f"\n✗ Error downloading {model_name}: {e}")

# 3. Verify installations
print("\n[3/3] Verifying installations...")
print("-" * 60)

try:
    import cv2
    print(f"✓ OpenCV: {cv2.__version__}")
except ImportError:
    print("✗ OpenCV not installed")

try:
    from ultralytics import YOLO
    print("✓ Ultralytics YOLO installed")
except ImportError:
    print("✗ Ultralytics not installed")

try:
    from segment_anything import sam_model_registry
    print("✓ Segment Anything (SAM) installed")
except ImportError:
    print("✗ SAM not installed")

try:
    import torch
    print(f"✓ PyTorch: {torch.__version__}")
    print(f"✓ CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"✓ CUDA Device: {torch.cuda.get_device_name(0)}")
except ImportError:
    print("✗ PyTorch not installed")

print("\n" + "=" * 60)
print("SETUP COMPLETE!")
print("=" * 60)
print("\nModels location:", MODELS_DIR.absolute())
print("\nYou can now run:")
print("  python python/detection/yolo_detector.py")
print("  python python/notebooks/01_yolo_test.ipynb")
