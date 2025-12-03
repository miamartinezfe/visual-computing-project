"""
YOLO Detector Class
Handles object detection using YOLOv8 models.
"""
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from ultralytics import YOLO
import time


class YOLODetector:
    """
    YOLO-based object detector for real-time detection.
    """
    
    def __init__(
        self,
        model_path: str = "yolov8n.pt",
        confidence: float = 0.5,
        iou_threshold: float = 0.45,
        device: str = "cuda"
    ):
        """
        Initialize YOLO detector.
        
        Args:
            model_path: Path to YOLO model weights
            confidence: Confidence threshold for detections
            iou_threshold: IoU threshold for NMS
            device: Device to run inference on ('cuda' or 'cpu')
        """
        self.model_path = model_path
        self.confidence = confidence
        self.iou_threshold = iou_threshold
        self.device = device
        
        print(f"Loading YOLO model: {model_path}")
        self.model = YOLO(model_path)
        self.model.to(device)
        
        # Get class names
        self.class_names = self.model.names
        print(f"✓ Model loaded on {device}")
        print(f"✓ Total classes: {len(self.class_names)}")
        
    def detect(
        self,
        image: np.ndarray,
        classes: Optional[List[int]] = None
    ) -> List[Dict]:
        """
        Perform object detection on an image.
        
        Args:
            image: Input image (BGR format)
            classes: List of class indices to detect (None for all)
            
        Returns:
            List of detection dictionaries containing:
                - bbox: [x1, y1, x2, y2]
                - confidence: float
                - class_id: int
                - class_name: str
        """
        start_time = time.time()
        
        # Run inference
        results = self.model.predict(
            image,
            conf=self.confidence,
            iou=self.iou_threshold,
            classes=classes,
            verbose=False
        )
        
        detections = []
        
        # Process results
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Extract box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0].cpu().numpy())
                cls_id = int(box.cls[0].cpu().numpy())
                
                detection = {
                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                    'confidence': conf,
                    'class_id': cls_id,
                    'class_name': self.class_names[cls_id]
                }
                detections.append(detection)
        
        inference_time = time.time() - start_time
        
        return detections, inference_time
    
    def detect_video(
        self,
        video_path: str,
        output_path: Optional[str] = None,
        display: bool = True,
        classes: Optional[List[int]] = None
    ) -> Dict:
        """
        Perform detection on video.
        
        Args:
            video_path: Path to input video
            output_path: Path to save output video (optional)
            display: Whether to display video during processing
            classes: List of class indices to detect
            
        Returns:
            Dictionary with statistics
        """
        cap = cv2.VideoCapture(video_path)
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"Processing video: {video_path}")
        print(f"Resolution: {width}x{height}, FPS: {fps}, Frames: {total_frames}")
        
        # Video writer
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        total_detections = 0
        total_time = 0
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Detect objects
                detections, inference_time = self.detect(frame, classes)
                total_time += inference_time
                total_detections += len(detections)
                
                # Annotate frame
                annotated_frame = self.draw_detections(frame, detections)
                
                # Add FPS info
                current_fps = 1 / inference_time if inference_time > 0 else 0
                cv2.putText(
                    annotated_frame,
                    f"FPS: {current_fps:.1f} | Detections: {len(detections)}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                
                # Save frame
                if writer:
                    writer.write(annotated_frame)
                
                # Display
                if display:
                    cv2.imshow('YOLO Detection', annotated_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                frame_count += 1
                if frame_count % 30 == 0:
                    print(f"Processed {frame_count}/{total_frames} frames...")
                    
        finally:
            cap.release()
            if writer:
                writer.release()
            if display:
                cv2.destroyAllWindows()
        
        # Statistics
        avg_fps = frame_count / total_time if total_time > 0 else 0
        avg_detections = total_detections / frame_count if frame_count > 0 else 0
        
        stats = {
            'total_frames': frame_count,
            'total_detections': total_detections,
            'avg_detections_per_frame': avg_detections,
            'total_time': total_time,
            'avg_fps': avg_fps
        }
        
        print(f"\nProcessing complete!")
        print(f"Avg FPS: {avg_fps:.2f}")
        print(f"Avg detections/frame: {avg_detections:.2f}")
        
        return stats
    
    def draw_detections(
        self,
        image: np.ndarray,
        detections: List[Dict],
        thickness: int = 2
    ) -> np.ndarray:
        """
        Draw bounding boxes and labels on image.
        
        Args:
            image: Input image
            detections: List of detection dictionaries
            thickness: Line thickness for boxes
            
        Returns:
            Annotated image
        """
        annotated = image.copy()
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            conf = det['confidence']
            label = det['class_name']
            
            # Draw bounding box
            color = self._get_color(det['class_id'])
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)
            
            # Draw label background
            label_text = f"{label} {conf:.2f}"
            (text_width, text_height), baseline = cv2.getTextSize(
                label_text,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                1
            )
            
            cv2.rectangle(
                annotated,
                (x1, y1 - text_height - baseline - 5),
                (x1 + text_width, y1),
                color,
                -1
            )
            
            # Draw label text
            cv2.putText(
                annotated,
                label_text,
                (x1, y1 - baseline - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1
            )
        
        return annotated
    
    def _get_color(self, class_id: int) -> Tuple[int, int, int]:
        """Generate a consistent color for each class."""
        np.random.seed(class_id)
        return tuple(map(int, np.random.randint(0, 255, 3)))
    
    def get_class_names(self) -> Dict[int, str]:
        """Get dictionary of class ID to name mappings."""
        return self.class_names


def main():
    """Demo usage of YOLODetector."""
    # Initialize detector
    detector = YOLODetector(
        model_path="yolov8n.pt",
        confidence=0.5,
        device="cuda"
    )
    
    # Test with sample image (if available)
    test_image_path = "data/input/test.jpg"
    
    if Path(test_image_path).exists():
        image = cv2.imread(test_image_path)
        detections, inference_time = detector.detect(image)
        
        print(f"\nDetections: {len(detections)}")
        print(f"Inference time: {inference_time*1000:.2f} ms")
        print(f"FPS: {1/inference_time:.2f}")
        
        # Draw and save results
        annotated = detector.draw_detections(image, detections)
        output_path = "results/images/yolo_test_output.jpg"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(output_path, annotated)
        print(f"Saved: {output_path}")
        
        # Display detections
        for i, det in enumerate(detections, 1):
            print(f"{i}. {det['class_name']}: {det['confidence']:.2f}")
    else:
        print(f"No test image found at {test_image_path}")
        print("Please add a test image and run again.")


if __name__ == "__main__":
    main()
