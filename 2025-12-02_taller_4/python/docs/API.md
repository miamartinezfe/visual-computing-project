# API Documentation - Detection & Segmentation

## Overview

REST API for object detection and segmentation using YOLOv8 and SAM (Segment Anything Model).

**Base URL**: `http://localhost:5000`

**Authentication**: None (for development)

---


## Starting the Server

```bash
# Basic
python api/server.py

# Custom host and port
python api/server.py --host 0.0.0.0 --port 8080

# Debug mode
python api/server.py --debug
```

---

## Limpieza automática de imágenes

Al cerrar el servidor, **todas las imágenes** generadas en `data/output/web_results` y subidas en `data/input/web_uploads` se eliminan automáticamente.

---

## Endpoints

### GET /

**Description**: API documentation and available endpoints

**Response**:
```json
{
  "name": "Detection & Segmentation API",
  "version": "1.0.0",
  "endpoints": { ... }
}
```

---

### GET /health

**Description**: Health check

**Response**:
```json
{
  "status": "healthy",
  "timestamp": 1701532800.0,
  "models_loaded": {
    "pipeline": true,
    "yolo": true,
    "sam": true
  }
}
```

---

### POST /detect

**Description**: Detect objects in an image using YOLO

**Content-Type**: 
- `multipart/form-data` (file upload)
- `application/json` (base64 image)

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image | file/string | Yes | Image file or base64 encoded string |
| confidence | float | No | Detection confidence threshold (0.0-1.0) |
| classes | string | No | Comma-separated class IDs to detect |
| return_image | boolean | No | Return annotated image (default: false) |

**Example Request** (cURL - File Upload):
```bash
curl -X POST http://localhost:5000/detect \
  -F "image=@test.jpg" \
  -F "confidence=0.6" \
  -F "return_image=true"
```

**Example Request** (cURL - Base64):
```bash
curl -X POST http://localhost:5000/detect \
  -H "Content-Type: application/json" \
  -d '{
    "image": "<base64_encoded_image>",
    "confidence": 0.6
  }'
```

**Example Request** (Python):
```python
import requests

# File upload
with open('test.jpg', 'rb') as f:
    files = {'image': f}
    data = {'confidence': 0.6, 'return_image': 'true'}
    response = requests.post('http://localhost:5000/detect', files=files, data=data)

# Base64
import base64
with open('test.jpg', 'rb') as f:
    img_base64 = base64.b64encode(f.read()).decode('utf-8')

response = requests.post(
    'http://localhost:5000/detect',
    json={'image': img_base64, 'confidence': 0.6}
)
```

**Response**:
```json
{
  "num_detections": 3,
  "inference_time_ms": 524.08,
  "total_time_ms": 550.23,
  "detections": [
    {
      "bbox": [100, 150, 300, 400],
      "confidence": 0.87,
      "class_id": 0,
      "class_name": "person"
    },
    {
      "bbox": [350, 100, 600, 500],
      "confidence": 0.92,
      "class_id": 5,
      "class_name": "bus"
    }
  ],
  "annotated_image": "<base64_encoded_image>"  // Only if return_image=true
}
```

---

### POST /segment

**Description**: Segment objects using SAM

**Content-Type**: 
- `multipart/form-data` (file upload)
- `application/json`

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image | file/string | Yes | Image file or base64 encoded string |
| bboxes | JSON array | Yes | List of bounding boxes [[x1,y1,x2,y2], ...] |
| return_image | boolean | No | Return annotated image (default: false) |

**Example Request** (Python):
```python
import requests

with open('test.jpg', 'rb') as f:
    files = {'image': f}
    data = {
        'bboxes': '[[100,150,300,400], [350,100,600,500]]',
        'return_image': 'true'
    }
    response = requests.post('http://localhost:5000/segment', files=files, data=data)

result = response.json()
```

**Response**:
```json
{
  "num_segments": 2,
  "total_time_ms": 58.34,
  "segments": [
    {
      "bbox": [100, 150, 300, 400],
      "segmentation_score": 0.95,
      "mask_area": 25600
    },
    {
      "bbox": [350, 100, 600, 500],
      "segmentation_score": 0.98,
      "mask_area": 48000
    }
  ],
  "annotated_image": "<base64_encoded_image>"  // Only if return_image=true
}
```

---

### POST /pipeline

**Description**: Complete detection + segmentation pipeline

**Content-Type**: 
- `multipart/form-data` (file upload)
- `application/json`

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image | file/string | Yes | Image file or base64 encoded string |
| save_masks | boolean | No | Save individual masks (default: false) |
| return_image | boolean | No | Return annotated image (default: true) |

**Example Request** (Python):
```python
import requests

with open('test.jpg', 'rb') as f:
    files = {'image': f}
    data = {'save_masks': 'true', 'return_image': 'true'}
    response = requests.post('http://localhost:5000/pipeline', files=files, data=data)

result = response.json()
print(f"Detections: {result['num_detections']}")
print(f"Total time: {result['total_time_ms']:.2f} ms")
```

**Response**:
```json
{
  "num_detections": 3,
  "detection_time_ms": 524.08,
  "segmentation_time_ms": 57.97,
  "total_time_ms": 1551.62,
  "fps": 0.64,
  "detections": [
    {
      "bbox": [100, 150, 300, 400],
      "confidence": 0.87,
      "class_id": 0,
      "class_name": "person",
      "segmentation_score": 0.95
    }
  ],
  "annotated_image": "<base64_encoded_image>"
}
```

---

### GET /models

**Description**: List available models

**Response**:
```json
{
  "yolo_models": ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"],
  "sam_models": ["sam_vit_b_01ec64.pth"],
  "currently_loaded": {
    "yolo": "yolov8n.pt",
    "sam": "sam_vit_b_01ec64.pth"
  }
}
```

---

### GET /config

**Description**: Get current configuration

**Response**:
```json
{
  "models": {
    "yolo": {
      "model_name": "yolov8n.pt",
      "confidence": 0.5,
      "device": "cuda"
    },
    "sam": {
      "model_type": "vit_b",
      "device": "cuda"
    }
  }
}
```

---

### GET /image/<filename>

**Description**: Retrieve a processed image

**Parameters**:
- `filename`: Name of the image file

**Example**: `http://localhost:5000/image/detection_result.jpg`

**Response**: Image file (JPEG)

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message description"
}
```

**Common HTTP Status Codes**:
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (resource doesn't exist)
- `500`: Internal Server Error

---

## Complete Example - Full Workflow

```python
import requests
import base64
import json
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:5000"

# 1. Check API health
response = requests.get(f"{BASE_URL}/health")
print("API Status:", response.json()['status'])

# 2. Upload image for detection
image_path = "test.jpg"
with open(image_path, 'rb') as f:
    files = {'image': f}
    data = {'confidence': 0.5, 'return_image': 'false'}
    response = requests.post(f"{BASE_URL}/detect", files=files, data=data)

detections = response.json()
print(f"Found {detections['num_detections']} objects")

# 3. Use pipeline for complete processing
with open(image_path, 'rb') as f:
    files = {'image': f}
    data = {'save_masks': 'true', 'return_image': 'true'}
    response = requests.post(f"{BASE_URL}/pipeline", files=files, data=data)

result = response.json()

# 4. Save annotated image if returned
if 'annotated_image' in result:
    img_data = base64.b64decode(result['annotated_image'])
    with open('result.jpg', 'wb') as f:
        f.write(img_data)
    print("Annotated image saved!")

# 5. Print results
print(f"\nResults:")
print(f"  Detections: {result['num_detections']}")
print(f"  Detection time: {result['detection_time_ms']:.2f} ms")
print(f"  Segmentation time: {result['segmentation_time_ms']:.2f} ms")
print(f"  Total time: {result['total_time_ms']:.2f} ms")
print(f"  FPS: {result['fps']:.2f}")

for i, det in enumerate(result['detections'], 1):
    print(f"\n  {i}. {det['class_name']}")
    print(f"     Confidence: {det['confidence']:.2f}")
    print(f"     Bbox: {det['bbox']}")
    if 'segmentation_score' in det:
        print(f"     Segmentation: {det['segmentation_score']:.2f}")
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production use, consider adding rate limiting middleware.

---

## CORS

CORS is enabled for all origins in development mode. Configure appropriately for production.

---

## File Size Limits

- Maximum upload size: **10 MB**
- Supported formats: PNG, JPG, JPEG, BMP, WEBP

---

## Performance Tips

1. **Use GPU**: Set `device: "cuda"` in config for 10-20x speed improvement
2. **Batch processing**: For multiple images, reuse the API connection
3. **Confidence threshold**: Higher thresholds reduce false positives and speed up processing
4. **Return images**: Set `return_image=false` if you don't need the annotated image (faster)

---

## Troubleshooting

### Models not loading
- Check that models are downloaded in `data/models/`
- Run `python download_models.py`

### Slow performance
- Enable GPU in `config.yaml`
- Use smaller YOLO model (`yolov8n.pt`)
- Increase confidence threshold

### Out of memory
- Reduce image size before sending
- Use CPU mode if GPU memory is limited
- Process fewer images concurrently

---

## Next Steps

- Integrate with your application
- Customize confidence thresholds
- Filter by specific object classes
- Build a frontend UI

For more examples, see [USAGE.md](USAGE.md)
