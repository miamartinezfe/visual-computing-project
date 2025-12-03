"""
Detection and Segmentation Pipeline
Integrates YOLO detection with SAM segmentation for complete analysis.
"""
import cv2
import numpy as np
import yaml
from pathlib import Path
from typing import List, Dict, Optional
import time
import json
import sys

# Handle imports for both module and standalone execution
try:
    from .yolo_detector import YOLODetector
    from .sam_segmenter import SAMSegmenter
except ImportError:
    # Running as standalone script
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from python.detection.yolo_detector import YOLODetector
    from python.detection.sam_segmenter import SAMSegmenter


class DetectionSegmentationPipeline:
    """
    Complete pipeline for detection and segmentation.
    Combines YOLO for fast detection and SAM for precise segmentation.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the pipeline.
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        print("=" * 60)
        print("INITIALIZING DETECTION & SEGMENTATION PIPELINE")
        print("=" * 60)
        
        # Initialize YOLO detector
        yolo_config = self.config['models']['yolo']
        self.detector = YOLODetector(
            model_path=yolo_config['model_name'],
            confidence=yolo_config['confidence'],
            iou_threshold=yolo_config['iou_threshold'],
            device=yolo_config['device']
        )
        
        # Initialize SAM segmenter
        sam_config = self.config['models']['sam']
        checkpoint_path = Path(self.config['io']['models_dir']) / sam_config['checkpoint']
        self.segmenter = SAMSegmenter(
            model_type=sam_config['model_type'],
            checkpoint_path=str(checkpoint_path),
            device=sam_config['device']
        )
        
        print("=" * 60)
        print("PIPELINE READY")
        print("=" * 60)
    
    def process_image(
        self,
        image_path: str,
        output_path: Optional[str] = None,
        save_masks: bool = True,
        save_json: bool = True
    ) -> Dict:
        """
        Process a single image through the complete pipeline.
        
        Args:
            image_path: Path to input image
            output_path: Path to save annotated image
            save_masks: Whether to save individual masks
            save_json: Whether to save detection data as JSON
            
        Returns:
            Dictionary with results and metrics
        """
        print(f"\nProcessing: {image_path}")
        start_time = time.time()
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        h, w = image.shape[:2]
        print(f"Image size: {w}x{h}")
        
        # Step 1: Detect objects
        print("Step 1/3: Detecting objects with YOLO...")
        detections, det_time = self.detector.detect(image)
        print(f"  ✓ Found {len(detections)} objects in {det_time*1000:.2f} ms")
        
        # Step 2: Segment objects
        if len(detections) > 0:
            print("Step 2/3: Segmenting objects with SAM...")
            detections, seg_time = self.segmenter.segment_detections(image, detections)
            print(f"  ✓ Segmented in {seg_time*1000:.2f} ms/object")
        else:
            seg_time = 0
            print("Step 2/3: No objects to segment")
        
        # Step 3: Visualize results
        print("Step 3/3: Creating visualization...")
        result_image = self._create_visualization(image, detections)
        
        # Save outputs
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(output_path), result_image)
            print(f"  ✓ Saved image: {output_path}")
        
        # Save individual masks
        if save_masks and len(detections) > 0:
            mask_dir = Path(output_path).parent / "masks" if output_path else Path("results/images/masks")
            self.segmenter.save_masks(detections, str(mask_dir))
        
        # Save JSON
        if save_json:
            json_path = Path(output_path).with_suffix('.json') if output_path else Path("results/images/detections.json")
            self._save_json(detections, json_path, det_time, seg_time)
            print(f"  ✓ Saved JSON: {json_path}")
        
        total_time = time.time() - start_time
        
        # Prepare results
        results = {
            'image_path': image_path,
            'image_size': (w, h),
            'num_detections': len(detections),
            'detection_time': det_time,
            'segmentation_time': seg_time * len(detections) if detections else 0,
            'total_time': total_time,
            'fps': 1 / total_time,
            'detections': detections
        }
        
        print(f"\n{'='*60}")
        print(f"RESULTS SUMMARY")
        print(f"{'='*60}")
        print(f"Total objects: {len(detections)}")
        print(f"Detection time: {det_time*1000:.2f} ms")
        print(f"Segmentation time: {seg_time*len(detections)*1000:.2f} ms" if detections else "Segmentation time: 0 ms")
        print(f"Total time: {total_time*1000:.2f} ms")
        print(f"FPS: {results['fps']:.2f}")
        print(f"{'='*60}")
        
        return results
    
    def process_video(
        self,
        video_path: str,
        output_path: Optional[str] = None,
        display: bool = False,
        process_every_n_frames: int = 1,
        max_frames: Optional[int] = None
    ) -> Dict:
        """
        Process video through the pipeline.
        
        Args:
            video_path: Path to input video
            output_path: Path to save output video
            display: Whether to display video during processing
            process_every_n_frames: Process every nth frame
            max_frames: Maximum frames to process
            
        Returns:
            Dictionary with statistics
        """
        print(f"\n{'='*60}")
        print(f"PROCESSING VIDEO")
        print(f"{'='*60}")
        
        cap = cv2.VideoCapture(video_path)
        
        # Video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if max_frames:
            total_frames = min(total_frames, max_frames)
        
        print(f"Video: {video_path}")
        print(f"Resolution: {width}x{height}")
        print(f"FPS: {fps}")
        print(f"Total frames: {total_frames}")
        print(f"Processing every {process_every_n_frames} frame(s)")
        
        # Video writer
        writer = None
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        frame_count = 0
        processed_count = 0
        total_detections = 0
        total_det_time = 0
        total_seg_time = 0
        start_time = time.time()
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret or (max_frames and frame_count >= max_frames):
                    break
                
                # Process frame
                if frame_count % process_every_n_frames == 0:
                    # Detect
                    detections, det_time = self.detector.detect(frame)
                    total_det_time += det_time
                    total_detections += len(detections)
                    
                    # Segment
                    if len(detections) > 0:
                        detections, seg_time = self.segmenter.segment_detections(frame, detections)
                        total_seg_time += seg_time * len(detections)
                    
                    # Visualize
                    annotated = self._create_visualization(frame, detections)
                    
                    # Add info overlay
                    current_fps = 1 / (det_time + seg_time * len(detections)) if detections else 1 / det_time
                    self._add_info_overlay(annotated, len(detections), current_fps, frame_count)
                    
                    processed_count += 1
                else:
                    annotated = frame
                
                # Save frame
                if writer:
                    writer.write(annotated)
                
                # Display
                if display:
                    cv2.imshow('Detection & Segmentation', annotated)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                frame_count += 1
                if frame_count % 30 == 0:
                    elapsed = time.time() - start_time
                    eta = (elapsed / frame_count) * (total_frames - frame_count)
                    print(f"Progress: {frame_count}/{total_frames} frames | ETA: {eta:.1f}s")
        
        finally:
            cap.release()
            if writer:
                writer.release()
            if display:
                cv2.destroyAllWindows()
        
        total_time = time.time() - start_time
        
        # Statistics
        stats = {
            'video_path': video_path,
            'total_frames': frame_count,
            'processed_frames': processed_count,
            'total_detections': total_detections,
            'avg_detections_per_frame': total_detections / processed_count if processed_count > 0 else 0,
            'total_detection_time': total_det_time,
            'total_segmentation_time': total_seg_time,
            'total_processing_time': total_time,
            'avg_fps': processed_count / total_time if total_time > 0 else 0,
            'output_path': str(output_path) if output_path else None
        }
        
        print(f"\n{'='*60}")
        print(f"VIDEO PROCESSING COMPLETE")
        print(f"{'='*60}")
        print(f"Frames processed: {processed_count}/{frame_count}")
        print(f"Total detections: {total_detections}")
        print(f"Avg detections/frame: {stats['avg_detections_per_frame']:.2f}")
        print(f"Avg FPS: {stats['avg_fps']:.2f}")
        print(f"Total time: {total_time:.2f}s")
        if output_path:
            print(f"Output saved: {output_path}")
        print(f"{'='*60}")
        
        return stats
    
    def _create_visualization(
        self,
        image: np.ndarray,
        detections: List[Dict]
    ) -> np.ndarray:
        """Create visualization with bounding boxes and masks."""
        # Start with detection boxes
        result = self.detector.draw_detections(image, detections)
        
        # Add segmentation masks if available
        if detections and 'mask' in detections[0]:
            result = self.segmenter.visualize_detections_with_masks(
                result, detections, alpha=0.3
            )
        
        return result
    
    def _add_info_overlay(
        self,
        image: np.ndarray,
        num_detections: int,
        fps: float,
        frame_num: int
    ):
        """Add information overlay to image."""
        overlay_text = [
            f"Frame: {frame_num}",
            f"Detections: {num_detections}",
            f"FPS: {fps:.1f}"
        ]
        
        y_offset = 30
        for text in overlay_text:
            cv2.putText(
                image,
                text,
                (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
            y_offset += 30
    
    def _save_json(
        self,
        detections: List[Dict],
        output_path: Path,
        det_time: float,
        seg_time: float
    ):
        """Save detection data to JSON."""
        # Prepare JSON-serializable data
        json_data = {
            'num_detections': len(detections),
            'detection_time_ms': det_time * 1000,
            'segmentation_time_ms': seg_time * 1000 * len(detections) if detections else 0,
            'detections': []
        }
        
        for det in detections:
            det_data = {
                'bbox': det['bbox'],
                'confidence': float(det['confidence']),
                'class_id': int(det['class_id']),
                'class_name': det['class_name']
            }
            
            if 'seg_score' in det:
                det_data['segmentation_score'] = float(det['seg_score'])
            
            json_data['detections'].append(det_data)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(json_data, f, indent=2)


def main():
    """Demo usage of the pipeline."""
    # Initialize pipeline
    pipeline = DetectionSegmentationPipeline(config_path="config.yaml")
    
    # Process test image
    test_image = "data/input/test.jpg"
    if Path(test_image).exists():
        results = pipeline.process_image(
            test_image,
            output_path="results/images/pipeline_output.jpg",
            save_masks=True,
            save_json=True
        )
        
        print("\nDetected objects:")
        for i, det in enumerate(results['detections'], 1):
            print(f"{i}. {det['class_name']}: {det['confidence']:.2f}")


if __name__ == "__main__":
    main()
