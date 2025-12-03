# Installation Guide - Detection & Segmentation Subsystem

## Prerequisites

- **Python 3.8+** (tested with 3.10 and 3.13)
- **Conda** environment manager
- **CUDA-capable GPU** (recommended, GTX 1650 or better)
- **8GB+ RAM**
- **2GB+ free disk space** for models

## Step 1: Create Conda Environment

```bash
# Create new environment
conda create -n cv_subsystem python=3.10 -y

# Activate environment
conda activate cv_subsystem
```

## Step 2: Install Dependencies

### Option A: Install from requirements.txt (Recommended)

```bash
pip install -r requirements.txt
```

### Option B: Manual Installation

```bash
# Core deep learning
pip install torch torchvision

# YOLO detection
pip install ultralytics

# SAM segmentation
pip install git+https://github.com/facebookresearch/segment-anything.git

# Image processing
pip install opencv-python Pillow

# Visualization and data
pip install matplotlib seaborn pandas numpy


# Backend
pip install flask flask-cors

# Utilities
pip install pyyaml tqdm imageio imageio-ffmpeg python-dotenv psutil
```

---

## Limpieza automática de imágenes

Al cerrar el servidor web, **todas las imágenes** generadas en `data/output/web_results` y subidas en `data/input/web_uploads` se eliminan automáticamente.

## Step 3: Download Models

Run the model download script:

```bash
python scripts/download_models.py
```

This will download:
- **YOLOv8 models** (nano, small, medium) - ~77 MB total
- **SAM model** (vit_b) - ~375 MB

Models are saved to `data/models/`

## Step 4: Download Sample Images (Optional)

```bash
python download_samples.py
```

This downloads test images to `data/input/`

## Step 5: Verify Installation

```bash
# Test YOLO detector
python python/detection/yolo_detector.py

# Test SAM segmenter
python python/detection/sam_segmenter.py

# Test complete pipeline
python python/detection/pipeline.py
```

## Troubleshooting

### CUDA Not Available

If you don't have a CUDA-capable GPU:

1. Edit `config.yaml`
2. Change `device: "cuda"` to `device: "cpu"` for both YOLO and SAM
3. Expect 5-10x slower performance

### Out of Memory

If you encounter GPU memory errors:

1. Use smaller YOLO model: `yolov8n.pt` instead of `yolov8m.pt`
2. Reduce batch processing
3. Process every Nth frame in videos

### Import Errors

Ensure you're using the correct Python environment:

```bash
# Check active environment
conda info --envs

# Activate if needed
conda activate cv_subsystem

# Verify Python
python --version
```

### Model Download Failures

If automatic download fails:

**YOLO models:**
- Download manually from: https://github.com/ultralytics/assets/releases
- Place in project root or `data/models/`

**SAM models:**
- Download from: https://github.com/facebookresearch/segment-anything#model-checkpoints
- Place `sam_vit_b_01ec64.pth` in `data/models/`

## System Requirements

### Minimum
- CPU: Intel i5 or equivalent
- RAM: 8GB
- GPU: Optional (CPU mode available)
- Storage: 5GB

### Recommended
- CPU: Intel i7 or equivalent
- RAM: 16GB
- GPU: NVIDIA GTX 1650 or better with 4GB+ VRAM
- Storage: 10GB
- OS: Windows 10/11, Linux, macOS

## Next Steps

After successful installation:

1. Read [USAGE.md](USAGE.md) for usage examples
2. Check [API.md](API.md) for API documentation
3. See [EVIDENCIAS.md](EVIDENCIAS.md) for demo results

## Support

For issues:
1. Check error messages carefully
2. Verify all dependencies are installed
3. Ensure models are downloaded correctly
4. Check CUDA/GPU drivers if using GPU mode
