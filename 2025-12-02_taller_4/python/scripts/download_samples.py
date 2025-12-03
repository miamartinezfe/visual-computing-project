"""
Download sample images for testing detection and segmentation.
"""
import urllib.request
from pathlib import Path

# Create input directory
INPUT_DIR = Path("data/input")
INPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Downloading sample test images...")
print("=" * 60)

# Sample images
sample_images = {
    "test.jpg": "https://ultralytics.com/images/bus.jpg",
    "people.jpg": "https://ultralytics.com/images/zidane.jpg",
}

for filename, url in sample_images.items():
    output_path = INPUT_DIR / filename
    
    if output_path.exists():
        print(f"✓ {filename} already exists")
    else:
        try:
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, output_path)
            print(f"✓ {filename} downloaded")
        except Exception as e:
            print(f"✗ Failed to download {filename}: {e}")

print("\n" + "=" * 60)
print(f"Sample images saved to: {INPUT_DIR.absolute()}")
print("\nYou can now test detection with:")
print("  python python/detection/yolo_detector.py")
print("  python python/detection/sam_segmenter.py")
