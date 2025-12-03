def cleanup_web_uploads():
    """Clean up web uploads folder on server shutdown"""
    import shutil
    try:
        if UPLOAD_FOLDER.exists():
            for file in UPLOAD_FOLDER.glob('*'):
                try:
                    if file.is_file():
                        file.unlink()
                    elif file.is_dir():
                        shutil.rmtree(file)
                except Exception as e:
                    print(f"⚠️ Could not delete {file}: {e}")
            print("🧹 Web uploads cleaned up successfully!")
    except Exception as e:
        print(f"⚠️ Error cleaning up web uploads: {e}")
"""
Web Interface for Detection & Segmentation
Simple HTML/JS interface served by Flask
With webcam support!
"""
import os
import sys
from pathlib import Path
import cv2
import numpy as np

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from flask import Flask, render_template_string, request, jsonify, send_file, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import base64
import io
from PIL import Image
import time
import uuid

# Import detection modules
from python.detection.pipeline import DetectionSegmentationPipeline

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = Path("data/input/web_uploads")
OUTPUT_FOLDER = Path("data/output/web_results")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Global pipeline (lazy loading)
pipeline = None

def get_pipeline():
    global pipeline
    if pipeline is None:
        print("🔄 Loading models... (this may take a moment)")
        pipeline = DetectionSegmentationPipeline(config_path="config.yaml")
        print("✅ Models loaded!")
    return pipeline

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Detection & Segmentation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            text-align: center;
            padding: 30px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 30px;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        header p {
            color: #888;
            font-size: 1.1em;
        }
        
        /* Mode Tabs */
        .mode-tabs {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 30px;
        }
        
        .tab-btn {
            padding: 12px 30px;
            border: 2px solid rgba(255,255,255,0.2);
            background: transparent;
            color: #fff;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
        }
        
        .tab-btn:hover {
            border-color: #00d4ff;
            background: rgba(0, 212, 255, 0.1);
        }
        
        .tab-btn.active {
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            border-color: transparent;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        
        @media (max-width: 900px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }
        
        .panel {
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .panel h2 {
            font-size: 1.3em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .upload-zone {
            border: 2px dashed rgba(255,255,255,0.3);
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 20px;
        }
        
        .upload-zone:hover {
            border-color: #00d4ff;
            background: rgba(0, 212, 255, 0.05);
        }
        
        .upload-zone.dragover {
            border-color: #7b2cbf;
            background: rgba(123, 44, 191, 0.1);
        }
        
        .upload-zone input {
            display: none;
        }
        
        .upload-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        
        .btn {
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            color: #fff;
            font-size: 1em;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin: 5px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 212, 255, 0.4);
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-secondary {
            background: rgba(255,255,255,0.1);
        }
        
        .btn-danger {
            background: linear-gradient(90deg, #ff4757, #ff6b81);
        }
        
        .btn-success {
            background: linear-gradient(90deg, #2ed573, #7bed9f);
        }
        
        .image-preview, .video-preview {
            width: 100%;
            max-height: 400px;
            object-fit: contain;
            border-radius: 10px;
            margin-bottom: 15px;
            background: rgba(0,0,0,0.3);
        }
        
        .placeholder {
            width: 100%;
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            color: #666;
            margin-bottom: 15px;
        }
        
        .results-info {
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
        }
        
        .results-info h3 {
            font-size: 1em;
            margin-bottom: 10px;
            color: #00d4ff;
        }
        
        .detection-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .detection-item:last-child {
            border-bottom: none;
        }
        
        .confidence-bar {
            width: 100px;
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            border-radius: 4px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 15px;
        }
        
        .stat-box {
            background: rgba(0,0,0,0.2);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #00d4ff;
        }
        
        .stat-label {
            font-size: 0.8em;
            color: #888;
            margin-top: 5px;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .loading.active {
            display: block;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid rgba(255,255,255,0.1);
            border-top-color: #00d4ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .options {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .option-group {
            flex: 1;
            min-width: 150px;
        }
        
        .option-group label {
            display: block;
            margin-bottom: 5px;
            font-size: 0.9em;
            color: #888;
        }
        
        .option-group select {
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(0,0,0,0.3);
            color: #fff;
            font-size: 1em;
        }
        
        footer {
            text-align: center;
            padding: 30px;
            color: #666;
            margin-top: 30px;
        }
        
        .error-message {
            background: rgba(255, 0, 0, 0.2);
            border: 1px solid rgba(255, 0, 0, 0.3);
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            display: none;
        }
        
        .error-message.active {
            display: block;
        }
        
        /* Webcam specific */
        .webcam-container {
            position: relative;
        }
        
        #webcamVideo {
            width: 100%;
            border-radius: 10px;
            background: #000;
        }
        
        .webcam-status {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(0,0,0,0.7);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #ff4757;
        }
        
        .status-dot.active {
            background: #2ed573;
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .hidden {
            display: none !important;
        }
        
        /* Canvas for webcam capture */
        #captureCanvas {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 Detection & Segmentation</h1>
            <p>YOLO + SAM Pipeline | Visual Computing - Taller 4</p>
        </header>
        
        <!-- Mode Selection Tabs -->
        <div class="mode-tabs">
            <button class="tab-btn active" id="tabImage" onclick="switchMode('image')">📷 Image Upload</button>
            <button class="tab-btn" id="tabWebcam" onclick="switchMode('webcam')">🎥 Webcam</button>
        </div>
        
        <div class="main-content">
            <!-- Input Panel -->
            <div class="panel">
                <h2>📤 Input</h2>
                
                <!-- Image Upload Mode -->
                <div id="imageMode">
                    <div class="upload-zone" id="uploadZone">
                        <input type="file" id="fileInput" accept="image/*">
                        <div class="upload-icon">📷</div>
                        <p>Drag & drop an image or click to select</p>
                        <p style="color: #666; margin-top: 10px; font-size: 0.9em;">Supports: JPG, PNG, WEBP</p>
                    </div>
                    
                    <div id="previewContainer" style="display: none;">
                        <img id="previewImage" class="image-preview" alt="Preview">
                    </div>
                </div>
                
                <!-- Webcam Mode -->
                <div id="webcamMode" class="hidden">
                    <div class="webcam-container">
                        <video id="webcamVideo" autoplay playsinline></video>
                        <div class="webcam-status">
                            <div class="status-dot" id="statusDot"></div>
                            <span id="statusText">Camera Off</span>
                        </div>
                    </div>
                    <canvas id="captureCanvas"></canvas>
                </div>
                
                <div class="options">
                    <div class="option-group">
                        <label>YOLO Model</label>
                        <select id="modelSelect">
                            <option value="yolov8n">YOLOv8 Nano (Fast)</option>
                            <option value="yolov8s">YOLOv8 Small</option>
                            <option value="yolov8m">YOLOv8 Medium (Accurate)</option>
                        </select>
                    </div>
                    <div class="option-group">
                        <label>Confidence Threshold</label>
                        <select id="confSelect">
                            <option value="0.25">25%</option>
                            <option value="0.50">50%</option>
                            <option value="0.75">75%</option>
                        </select>
                    </div>
                </div>
                
                <!-- Image Mode Buttons -->
                <div id="imageButtons" style="text-align: center;">
                    <button class="btn" id="processBtn" disabled>🚀 Process Image</button>
                    <button class="btn btn-secondary" id="clearBtn">🗑️ Clear</button>
                </div>
                
                <!-- Webcam Mode Buttons -->
                <div id="webcamButtons" class="hidden" style="text-align: center;">
                    <button class="btn btn-success" id="startCamBtn">📹 Start Camera</button>
                    <button class="btn btn-danger hidden" id="stopCamBtn">⏹️ Stop Camera</button>
                    <button class="btn" id="captureBtn" disabled>📸 Capture & Analyze</button>
                    <button class="btn btn-secondary" id="autoModeBtn">🔄 Auto Mode: OFF</button>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Processing image...</p>
                    <p style="color: #666; font-size: 0.9em;">Running YOLO detection + SAM segmentation</p>
                </div>
                
                <div class="error-message" id="errorMessage"></div>
            </div>
            
            <!-- Output Panel -->
            <div class="panel">
                <h2>📊 Results</h2>
                
                <div id="resultPlaceholder" class="placeholder">
                    <p>Results will appear here</p>
                </div>
                
                <div id="resultContainer" style="display: none;">
                    <img id="resultImage" class="image-preview" alt="Result">
                    
                    <div class="stats-grid">
                        <div class="stat-box">
                            <div class="stat-value" id="objectCount">0</div>
                            <div class="stat-label">Objects</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value" id="processTime">0</div>
                            <div class="stat-label">Time (ms)</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value" id="fpsValue">0</div>
                            <div class="stat-label">FPS</div>
                        </div>
                    </div>
                    
                    <div class="results-info">
                        <h3>Detected Objects</h3>
                        <div id="detectionsList"></div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 15px;">
                        <button class="btn btn-secondary" id="downloadBtn">💾 Download Result</button>
                    </div>
                </div>
            </div>
        </div>
        
        <footer>
            <p>Visual Computing - Taller 4 | YOLO + SAM Detection & Segmentation Pipeline</p>
        </footer>
    </div>
    
    <script>
        // Elements - Image Mode
        const uploadZone = document.getElementById('uploadZone');
        const fileInput = document.getElementById('fileInput');
        const previewContainer = document.getElementById('previewContainer');
        const previewImage = document.getElementById('previewImage');
        const processBtn = document.getElementById('processBtn');
        const clearBtn = document.getElementById('clearBtn');
        
        // Elements - Webcam Mode
        const webcamVideo = document.getElementById('webcamVideo');
        const captureCanvas = document.getElementById('captureCanvas');
        const startCamBtn = document.getElementById('startCamBtn');
        const stopCamBtn = document.getElementById('stopCamBtn');
        const captureBtn = document.getElementById('captureBtn');
        const autoModeBtn = document.getElementById('autoModeBtn');
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        
        // Elements - Common
        const loading = document.getElementById('loading');
        const errorMessage = document.getElementById('errorMessage');
        const resultPlaceholder = document.getElementById('resultPlaceholder');
        const resultContainer = document.getElementById('resultContainer');
        const resultImage = document.getElementById('resultImage');
        const downloadBtn = document.getElementById('downloadBtn');
        
        // State
        let currentFile = null;
        let resultUrl = null;
        let webcamStream = null;
        let autoMode = false;
        let autoModeInterval = null;
        let isProcessing = false;
        
        // Mode switching
        function switchMode(mode) {
            document.getElementById('tabImage').classList.remove('active');
            document.getElementById('tabWebcam').classList.remove('active');
            document.getElementById('tab' + mode.charAt(0).toUpperCase() + mode.slice(1)).classList.add('active');
            
            if (mode === 'image') {
                document.getElementById('imageMode').classList.remove('hidden');
                document.getElementById('webcamMode').classList.add('hidden');
                document.getElementById('imageButtons').classList.remove('hidden');
                document.getElementById('webcamButtons').classList.add('hidden');
                stopWebcam();
            } else {
                document.getElementById('imageMode').classList.add('hidden');
                document.getElementById('webcamMode').classList.remove('hidden');
                document.getElementById('imageButtons').classList.add('hidden');
                document.getElementById('webcamButtons').classList.remove('hidden');
            }
        }
        
        // ==================== IMAGE MODE ====================
        
        // Drag & Drop
        uploadZone.addEventListener('click', () => fileInput.click());
        
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('dragover');
        });
        
        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('dragover');
        });
        
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                handleFile(e.dataTransfer.files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                handleFile(e.target.files[0]);
            }
        });
        
        function handleFile(file) {
            if (!file.type.startsWith('image/')) {
                showError('Please select an image file');
                return;
            }
            
            currentFile = file;
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                previewContainer.style.display = 'block';
                uploadZone.style.display = 'none';
                processBtn.disabled = false;
            };
            reader.readAsDataURL(file);
            hideError();
        }
        
        clearBtn.addEventListener('click', () => {
            currentFile = null;
            resultUrl = null;
            previewContainer.style.display = 'none';
            uploadZone.style.display = 'block';
            resultPlaceholder.style.display = 'flex';
            resultContainer.style.display = 'none';
            processBtn.disabled = true;
            fileInput.value = '';
            hideError();
        });
        
        processBtn.addEventListener('click', () => processImage(currentFile));
        
        // ==================== WEBCAM MODE ====================
        
        async function startWebcam() {
            try {
                webcamStream = await navigator.mediaDevices.getUserMedia({ 
                    video: { 
                        width: { ideal: 1280 },
                        height: { ideal: 720 },
                        facingMode: 'environment'
                    } 
                });
                webcamVideo.srcObject = webcamStream;
                
                statusDot.classList.add('active');
                statusText.textContent = 'Camera Active';
                
                startCamBtn.classList.add('hidden');
                stopCamBtn.classList.remove('hidden');
                captureBtn.disabled = false;
                
                hideError();
            } catch (error) {
                showError('Could not access camera: ' + error.message);
            }
        }
        
        function stopWebcam() {
            if (webcamStream) {
                webcamStream.getTracks().forEach(track => track.stop());
                webcamStream = null;
            }
            webcamVideo.srcObject = null;
            
            statusDot.classList.remove('active');
            statusText.textContent = 'Camera Off';
            
            startCamBtn.classList.remove('hidden');
            stopCamBtn.classList.add('hidden');
            captureBtn.disabled = true;
            
            // Stop auto mode
            if (autoMode) {
                toggleAutoMode();
            }
        }
        
        function captureFrame() {
            if (!webcamStream) return null;
            
            const video = webcamVideo;
            const canvas = captureCanvas;
            
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);
            
            return new Promise((resolve) => {
                canvas.toBlob((blob) => {
                    resolve(new File([blob], 'webcam_capture.jpg', { type: 'image/jpeg' }));
                }, 'image/jpeg', 0.9);
            });
        }
        
        async function captureAndProcess() {
            if (isProcessing || !webcamStream) return;
            
            const file = await captureFrame();
            if (file) {
                await processImage(file);
            }
        }
        
        function toggleAutoMode() {
            autoMode = !autoMode;
            
            if (autoMode) {
                autoModeBtn.textContent = '🔄 Auto Mode: ON';
                autoModeBtn.classList.add('btn-success');
                autoModeBtn.classList.remove('btn-secondary');
                
                // Process every 2 seconds
                autoModeInterval = setInterval(async () => {
                    if (!isProcessing && webcamStream) {
                        await captureAndProcess();
                    }
                }, 2000);
            } else {
                autoModeBtn.textContent = '🔄 Auto Mode: OFF';
                autoModeBtn.classList.remove('btn-success');
                autoModeBtn.classList.add('btn-secondary');
                
                if (autoModeInterval) {
                    clearInterval(autoModeInterval);
                    autoModeInterval = null;
                }
            }
        }
        
        startCamBtn.addEventListener('click', startWebcam);
        stopCamBtn.addEventListener('click', stopWebcam);
        captureBtn.addEventListener('click', captureAndProcess);
        autoModeBtn.addEventListener('click', toggleAutoMode);
        
        // ==================== COMMON PROCESSING ====================
        
        async function processImage(file) {
            if (!file || isProcessing) return;
            
            isProcessing = true;
            loading.classList.add('active');
            processBtn.disabled = true;
            captureBtn.disabled = true;
            hideError();
            
            const formData = new FormData();
            formData.append('image', file);
            formData.append('model', document.getElementById('modelSelect').value);
            formData.append('confidence', document.getElementById('confSelect').value);
            
            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    displayResults(data);
                } else {
                    showError(data.error || 'Processing failed');
                }
            } catch (error) {
                showError('Connection error: ' + error.message);
            } finally {
                loading.classList.remove('active');
                processBtn.disabled = !currentFile;
                captureBtn.disabled = !webcamStream;
                isProcessing = false;
            }
        }
        
        function displayResults(data) {
            console.log('=== API RESPONSE ===');
            console.log('Success:', data.success);
            console.log('Num detections:', data.num_detections);
            
            resultImage.src = 'data:image/jpeg;base64,' + data.image;
            resultUrl = data.image;
            
            document.getElementById('objectCount').textContent = data.num_detections;
            document.getElementById('processTime').textContent = Math.round(data.total_time * 1000);
            document.getElementById('fpsValue').textContent = (1 / data.total_time).toFixed(2);
            
            const detectionsList = document.getElementById('detectionsList');
            detectionsList.innerHTML = '';
            
            if (data.detections.length === 0) {
                detectionsList.innerHTML = '<p style="color: #888; text-align: center;">No objects detected</p>';
            } else {
                data.detections.forEach(det => {
                    const item = document.createElement('div');
                    item.className = 'detection-item';
                    item.innerHTML = `
                        <span>${det.class}</span>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span>${(det.confidence * 100).toFixed(1)}%</span>
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: ${det.confidence * 100}%"></div>
                            </div>
                        </div>
                    `;
                    detectionsList.appendChild(item);
                });
            }
            
            resultPlaceholder.style.display = 'none';
            resultContainer.style.display = 'block';
        }
        
        downloadBtn.addEventListener('click', () => {
            if (!resultUrl) return;
            
            const link = document.createElement('a');
            link.href = 'data:image/jpeg;base64,' + resultUrl;
            link.download = 'detection_result.jpg';
            link.click();
        });
        
        function showError(message) {
            errorMessage.textContent = '❌ ' + message;
            errorMessage.classList.add('active');
        }
        
        function hideError() {
            errorMessage.classList.remove('active');
        }
        
        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            stopWebcam();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/process', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Get options
        model = request.form.get('model', 'yolov8n')
        confidence = float(request.form.get('confidence', 0.25))
        
        # Save uploaded file with unique name
        unique_id = str(uuid.uuid4())[:8]
        original_name = secure_filename(file.filename)
        base_name = Path(original_name).stem
        extension = Path(original_name).suffix or '.jpg'
        
        filename = f"{base_name}_{unique_id}{extension}"
        filepath = UPLOAD_FOLDER / filename
        file.save(str(filepath))
        
        print(f"📁 Uploaded file saved to: {filepath}")
        
        # Define unique output path
        output_filename = f"result_{unique_id}.jpg"
        output_path = OUTPUT_FOLDER / output_filename
        
        print(f"📤 Output will be saved to: {output_path}")
        
        # Process with pipeline
        pipe = get_pipeline()
        
        start_time = time.time()
        results = pipe.process_image(
            str(filepath),
            output_path=str(output_path),
            save_masks=False,
            save_json=False
        )
        total_time = time.time() - start_time
        
        print(f"✅ Processing complete. Output exists: {output_path.exists()}")
        
        # Convert result image to base64
        with open(str(output_path), 'rb') as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        print(f"📊 Base64 image length: {len(img_base64)}")
        
        # Prepare detections
        detections = []
        for det in results.get('detections', []):
            # Handle both 'class_name' (from detector) and 'class' keys
            class_name = det.get('class_name') or det.get('class', 'unknown')
            detections.append({
                'class': class_name,
                'confidence': det.get('confidence', 0),
                'bbox': det.get('bbox', [])
            })
        
        return jsonify({
            'success': True,
            'image': img_base64,
            'num_detections': len(detections),
            'detections': detections,
            'total_time': total_time,
            'detection_time': results.get('detection_time', 0),
            'segmentation_time': results.get('segmentation_time', 0)
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'models_loaded': pipeline is not None})

def cleanup_web_results():
    """Clean up web results folder on server shutdown"""
    import shutil
    try:
        if OUTPUT_FOLDER.exists():
            # Remove all files in the output folder
            for file in OUTPUT_FOLDER.glob('*'):
                try:
                    if file.is_file():
                        file.unlink()
                    elif file.is_dir():
                        shutil.rmtree(file)
                except Exception as e:
                    print(f"⚠️ Could not delete {file}: {e}")
            print("🧹 Web results cleaned up successfully!")
    except Exception as e:
        print(f"⚠️ Error cleaning up web results: {e}")

if __name__ == '__main__':
    import atexit
    import signal
    
    # Register cleanup functions to run on exit
    atexit.register(cleanup_web_results)
    atexit.register(cleanup_web_uploads)
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n🛑 Shutting down server...")
        cleanup_web_results()
        cleanup_web_uploads()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║       🎯 DETECTION & SEGMENTATION WEB INTERFACE 🎯           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   Open your browser at:                                      ║
║                                                              ║
║       👉  http://localhost:8080                              ║
║                                                              ║
║   Features:                                                  ║
║   • 📷 Image upload with drag & drop                         ║
║   • 🎥 Live webcam capture & analysis                        ║
║   • 🔄 Auto-mode for continuous detection                    ║
║   • 🎯 YOLO object detection                                 ║
║   • 🖼️ SAM instance segmentation                             ║
║                                                              ║
║   Press Ctrl+C to stop the server                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=8080, debug=False)
