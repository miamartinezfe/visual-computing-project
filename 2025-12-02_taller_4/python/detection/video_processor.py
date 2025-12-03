"""
Video Processor
Process videos with webcam support using detection and segmentation pipeline.
"""
import cv2
import numpy as np
from pathlib import Path
from typing import Optional
import argparse
import sys
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from detection.pipeline import DetectionSegmentationPipeline


class VideoProcessor:
    """Process video files or webcam stream."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize video processor.
        
        Args:
            config_path: Path to configuration file
        """
        self.pipeline = DetectionSegmentationPipeline(config_path)
    
    def process_webcam(
        self,
        camera_id: int = 0,
        output_path: Optional[str] = None,
        max_duration: Optional[int] = None
    ):
        """
        Process webcam stream in real-time.
        
        Args:
            camera_id: Camera device ID
            output_path: Path to save output video
            max_duration: Maximum duration in seconds
        """
        print(f"\nOpening webcam (ID: {camera_id})...")
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_id}")
            return
        
        # Get camera properties
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Camera: {width}x{height} @ {fps} FPS")
        print("Press 'q' to quit, 's' to save screenshot")
        
        # Video writer
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            print(f"Recording to: {output_path}")
        
        frame_count = 0
        import time
        start_time = time.time()
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Check max duration
                if max_duration and (time.time() - start_time) > max_duration:
                    print(f"\nReached max duration: {max_duration}s")
                    break
                
                # Process frame
                detections, det_time = self.pipeline.detector.detect(frame)
                
                # Segment if detections found
                if len(detections) > 0:
                    detections, _ = self.pipeline.segmenter.segment_detections(
                        frame, detections
                    )
                
                # Visualize
                result = self.pipeline._create_visualization(frame, detections)
                
                # Add info
                elapsed = time.time() - start_time
                current_fps = frame_count / elapsed if elapsed > 0 else 0
                
                info_text = [
                    f"FPS: {current_fps:.1f}",
                    f"Detections: {len(detections)}",
                    f"Time: {elapsed:.1f}s"
                ]
                
                y_offset = 30
                for text in info_text:
                    cv2.putText(
                        result, text, (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 0), 2
                    )
                    y_offset += 35
                
                # Save frame
                if writer:
                    writer.write(result)
                
                # Display
                cv2.imshow('Webcam - Detection & Segmentation', result)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Save screenshot
                    screenshot_path = f"results/images/webcam_screenshot_{frame_count}.jpg"
                    cv2.imwrite(screenshot_path, result)
                    print(f"Screenshot saved: {screenshot_path}")
                
                frame_count += 1
        
        finally:
            cap.release()
            if writer:
                writer.release()
            cv2.destroyAllWindows()
            
            elapsed = time.time() - start_time
            print(f"\nProcessed {frame_count} frames in {elapsed:.2f}s")
            print(f"Average FPS: {frame_count/elapsed:.2f}")
    
    def process_file(
        self,
        video_path: str,
        output_path: Optional[str] = None,
        display: bool = True,
        process_every_n_frames: int = 1
    ):
        """
        Process video file.
        
        Args:
            video_path: Path to input video
            output_path: Path to save output
            display: Show video during processing
            process_every_n_frames: Process every nth frame
        """
        return self.pipeline.process_video(
            video_path=video_path,
            output_path=output_path,
            display=display,
            process_every_n_frames=process_every_n_frames
        )


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Video processor with object detection and segmentation"
    )
    
    parser.add_argument(
        '--source',
        type=str,
        default='webcam',
        help='Video source: "webcam", camera ID (0, 1, ...), or path to video file'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output video path'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--no-display',
        action='store_true',
        help='Disable video display'
    )
    
    parser.add_argument(
        '--process-every',
        type=int,
        default=1,
        help='Process every nth frame (for faster processing)'
    )
    
    parser.add_argument(
        '--max-duration',
        type=int,
        default=None,
        help='Maximum recording duration in seconds (webcam only)'
    )
    
    args = parser.parse_args()
    
    # Initialize processor
    processor = VideoProcessor(config_path=args.config)
    
    # Determine source
    if args.source == 'webcam' or args.source.isdigit():
        # Webcam mode
        camera_id = 0 if args.source == 'webcam' else int(args.source)
        processor.process_webcam(
            camera_id=camera_id,
            output_path=args.output,
            max_duration=args.max_duration
        )
    else:
        # Video file mode
        if not Path(args.source).exists():
            print(f"Error: Video file not found: {args.source}")
            return
        
        processor.process_file(
            video_path=args.source,
            output_path=args.output,
            display=not args.no_display,
            process_every_n_frames=args.process_every
        )


if __name__ == "__main__":
    main()
