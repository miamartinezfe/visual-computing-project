"""
Flask REST API for Detection and Segmentation
Provides HTTP endpoints for image processing.
"""
import os
import sys
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import base64
import io
from PIL import Image
import json
import time

# Add parent directory to path and import modules
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
project_root = parent_dir.parent

# Add to path
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(project_root))

# Change working directory to project root
os.chdir(project_root)

# Import detection modules
from python.detection.pipeline import DetectionSegmentationPipeline
from python.detection.yolo_detector import YOLODetector
from python.detection.sam_segmenter import SAMSegmenter

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'data/input/api_uploads'
OUTPUT_FOLDER = 'data/output/api_results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize pipeline (lazy loading)
pipeline = None
yolo_detector = None
sam_segmenter = None


def get_pipeline():
    """Get or initialize pipeline."""
    global pipeline
    if pipeline is None:
        print("Initializing detection & segmentation pipeline...")
        pipeline = DetectionSegmentationPipeline(config_path='config.yaml')
        print("Pipeline ready!")
    return pipeline


def get_yolo():
    """Get or initialize YOLO detector."""
    global yolo_detector
    if yolo_detector is None:
        print("Initializing YOLO detector...")
        yolo_detector = YOLODetector(model_path="yolov8n.pt", device="cuda")
        print("YOLO ready!")
    return yolo_detector


def get_sam():
    """Get or initialize SAM segmenter."""
    global sam_segmenter
    if sam_segmenter is None:
        print("Initializing SAM segmenter...")
        sam_segmenter = SAMSegmenter(
            model_type="vit_b",
            checkpoint_path="data/models/sam_vit_b_01ec64.pth",
            device="cuda"
        )
        print("SAM ready!")
    return sam_segmenter


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def encode_image_to_base64(image_path):
    """Encode image to base64 string."""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def decode_base64_image(base64_string):
    """Decode base64 string to image."""
    img_data = base64.b64decode(base64_string)
    img_array = np.frombuffer(img_data, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """API documentation."""
    return jsonify({
        'name': 'Detection & Segmentation API',
        'version': '1.0.0',
        'description': 'REST API for object detection and segmentation using YOLOv8 and SAM',
        'endpoints': {
            '/': 'GET - API documentation',
            '/health': 'GET - Health check',
            '/detect': 'POST - Detect objects in image',
            '/segment': 'POST - Segment objects in image',
            '/pipeline': 'POST - Complete detection + segmentation pipeline',
            '/models': 'GET - List available models',
            '/config': 'GET - Get current configuration'
        },
        'usage': {
            'upload': 'Send image as multipart/form-data with key "image"',
            'base64': 'Send image as JSON with key "image" (base64 encoded)'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'models_loaded': {
            'pipeline': pipeline is not None,
            'yolo': yolo_detector is not None,
            'sam': sam_segmenter is not None
        }
    })


@app.route('/models')
def list_models():
    """List available models."""
    models_dir = Path('data/models')
    
    yolo_models = list(Path('.').glob('yolov8*.pt'))
    sam_models = list(models_dir.glob('sam_*.pth'))
    
    return jsonify({
        'yolo_models': [m.name for m in yolo_models],
        'sam_models': [m.name for m in sam_models],
        'currently_loaded': {
            'yolo': 'yolov8n.pt' if yolo_detector else None,
            'sam': 'sam_vit_b_01ec64.pth' if sam_segmenter else None
        }
    })


@app.route('/config')
def get_config():
    """Get current configuration."""
    import yaml
    
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/detect', methods=['POST'])
def detect():
    """
    Detect objects in image.
    
    Input:
        - image: file upload or base64 string
        - confidence: float (optional, default from config)
        - classes: list of int (optional, specific classes to detect)
        - return_image: bool (optional, return annotated image)
    
    Returns:
        JSON with detections and optionally annotated image
    """
    try:
        # Get parameters
        confidence = request.form.get('confidence', type=float)
        classes = request.form.get('classes')
        if classes:
            classes = [int(c) for c in classes.split(',')]
        return_image = request.form.get('return_image', 'false').lower() == 'true'
        
        # Get image
        if 'image' in request.files:
            # File upload
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type'}), 400
            
            filename = secure_filename(file.filename)
            filepath = Path(app.config['UPLOAD_FOLDER']) / filename
            file.save(filepath)
            
            image = cv2.imread(str(filepath))
        
        elif request.json and 'image' in request.json:
            # Base64 encoded
            image = decode_base64_image(request.json['image'])
        
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        # Detect
        detector = get_yolo()
        if confidence:
            detector.confidence = confidence
        
        start_time = time.time()
        detections, inference_time = detector.detect(image, classes=classes)
        
        # Prepare response
        response = {
            'num_detections': len(detections),
            'inference_time_ms': inference_time * 1000,
            'total_time_ms': (time.time() - start_time) * 1000,
            'detections': []
        }
        
        for det in detections:
            response['detections'].append({
                'bbox': det['bbox'],
                'confidence': float(det['confidence']),
                'class_id': int(det['class_id']),
                'class_name': det['class_name']
            })
        
        # Add annotated image if requested
        if return_image:
            annotated = detector.draw_detections(image, detections)
            output_path = Path(app.config['OUTPUT_FOLDER']) / 'detection_result.jpg'
            cv2.imwrite(str(output_path), annotated)
            response['annotated_image'] = encode_image_to_base64(output_path)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/segment', methods=['POST'])
def segment():
    """
    Segment objects in image.
    
    Input:
        - image: file upload or base64 string
        - bboxes: JSON list of bounding boxes [[x1,y1,x2,y2], ...]
        - return_image: bool (optional, return annotated image)
    
    Returns:
        JSON with segmentation results
    """
    try:
        return_image = request.form.get('return_image', 'false').lower() == 'true'
        
        # Get image
        if 'image' in request.files:
            file = request.files['image']
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type'}), 400
            
            filename = secure_filename(file.filename)
            filepath = Path(app.config['UPLOAD_FOLDER']) / filename
            file.save(filepath)
            image = cv2.imread(str(filepath))
        
        elif request.json and 'image' in request.json:
            image = decode_base64_image(request.json['image'])
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        # Get bboxes
        if 'bboxes' in request.form:
            bboxes = json.loads(request.form.get('bboxes'))
        elif request.json and 'bboxes' in request.json:
            bboxes = request.json['bboxes']
        else:
            return jsonify({'error': 'No bounding boxes provided'}), 400
        
        # Segment
        segmenter = get_sam()
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        segmenter.set_image(rgb_image)
        
        start_time = time.time()
        results = []
        
        for bbox in bboxes:
            mask, score, seg_time = segmenter.segment_from_bbox(bbox)
            results.append({
                'bbox': bbox,
                'segmentation_score': float(score),
                'mask_area': int(mask.sum())
            })
        
        response = {
            'num_segments': len(results),
            'total_time_ms': (time.time() - start_time) * 1000,
            'segments': results
        }
        
        # Add visualization if requested
        if return_image:
            detections = [{'bbox': bbox, 'mask': mask} for bbox, res in zip(bboxes, results)]
            visualized = segmenter.visualize_detections_with_masks(image, detections)
            output_path = Path(app.config['OUTPUT_FOLDER']) / 'segmentation_result.jpg'
            cv2.imwrite(str(output_path), visualized)
            response['annotated_image'] = encode_image_to_base64(output_path)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/pipeline', methods=['POST'])
def pipeline_process():
    """
    Complete detection + segmentation pipeline.
    
    Input:
        - image: file upload or base64 string
        - save_masks: bool (optional)
        - return_image: bool (optional)
    
    Returns:
        JSON with complete results
    """
    try:
        save_masks = request.form.get('save_masks', 'false').lower() == 'true'
        return_image = request.form.get('return_image', 'true').lower() == 'true'
        
        # Get image
        if 'image' in request.files:
            file = request.files['image']
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type'}), 400
            
            filename = secure_filename(file.filename)
            filepath = Path(app.config['UPLOAD_FOLDER']) / filename
            file.save(filepath)
        
        elif request.json and 'image' in request.json:
            img = decode_base64_image(request.json['image'])
            filepath = Path(app.config['UPLOAD_FOLDER']) / 'temp_image.jpg'
            cv2.imwrite(str(filepath), img)
        
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        # Process through pipeline
        pipe = get_pipeline()
        output_path = Path(app.config['OUTPUT_FOLDER']) / 'pipeline_result.jpg'
        
        results = pipe.process_image(
            str(filepath),
            output_path=str(output_path) if return_image else None,
            save_masks=save_masks,
            save_json=False
        )
        
        # Prepare response
        response = {
            'num_detections': results['num_detections'],
            'detection_time_ms': results['detection_time'] * 1000,
            'segmentation_time_ms': results['segmentation_time'] * 1000,
            'total_time_ms': results['total_time'] * 1000,
            'fps': results['fps'],
            'detections': []
        }
        
        for det in results['detections']:
            det_data = {
                'bbox': det['bbox'],
                'confidence': float(det['confidence']),
                'class_id': int(det['class_id']),
                'class_name': det['class_name']
            }
            if 'seg_score' in det:
                det_data['segmentation_score'] = float(det['seg_score'])
            
            response['detections'].append(det_data)
        
        if return_image and output_path.exists():
            response['annotated_image'] = encode_image_to_base64(output_path)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/image/<filename>')
def get_image(filename):
    """Get processed image."""
    filepath = Path(app.config['OUTPUT_FOLDER']) / filename
    if filepath.exists():
        return send_file(filepath, mimetype='image/jpeg')
    return jsonify({'error': 'Image not found'}), 404


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the Flask server."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Detection & Segmentation API Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=5000, help='Port number')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print("="*60)
    print("DETECTION & SEGMENTATION API SERVER")
    print("="*60)
    print(f"Starting server on http://{args.host}:{args.port}")
    print("="*60)
    
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
