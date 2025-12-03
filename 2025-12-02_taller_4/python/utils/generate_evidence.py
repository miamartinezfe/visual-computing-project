"""
Generate Evidence Materials
Create videos, GIFs, and screenshots for documentation.
"""
import cv2
import numpy as np
from pathlib import Path
import sys
from PIL import Image
import imageio

sys.path.append(str(Path(__file__).parent.parent))

from detection.pipeline import DetectionSegmentationPipeline


def create_demo_video(
    input_path: str,
    output_path: str,
    duration: int = 30,
    process_every_n: int = 1
):
    """
    Create a demo video from webcam or video file.
    
    Args:
        input_path: 'webcam' or path to video file
        output_path: Path to save demo video
        duration: Maximum duration in seconds
        process_every_n: Process every nth frame
    """
    print(f"Creating demo video: {output_path}")
    
    # Initialize pipeline
    pipeline = DetectionSegmentationPipeline()
    
    # Open video source
    if input_path == 'webcam':
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source: {input_path}")
        return
    
    # Get properties
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Video writer
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    max_frames = duration * fps
    
    print(f"Recording for {duration}s at {fps} FPS...")
    
    try:
        while frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            if frame_count % process_every_n == 0:
                detections, det_time = pipeline.detector.detect(frame)
                
                if len(detections) > 0:
                    detections, _ = pipeline.segmenter.segment_detections(frame, detections)
                
                result = pipeline._create_visualization(frame, detections)
                
                # Add info overlay
                cv2.putText(
                    result,
                    f"Frame: {frame_count} | Detections: {len(detections)}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )
            else:
                result = frame
            
            writer.write(result)
            frame_count += 1
            
            if frame_count % 30 == 0:
                print(f"  Progress: {frame_count}/{max_frames} frames")
    
    finally:
        cap.release()
        writer.release()
    
    print(f"✓ Demo video saved: {output_path}")
    print(f"  Total frames: {frame_count}")


def video_to_gif(
    video_path: str,
    output_path: str,
    start_time: float = 0,
    duration: float = 5,
    fps: int = 10,
    scale: float = 0.5
):
    """
    Convert video segment to GIF.
    
    Args:
        video_path: Path to video file
        output_path: Path to save GIF
        start_time: Start time in seconds
        duration: Duration in seconds
        fps: GIF frame rate
        scale: Scale factor for size reduction
    """
    print(f"Creating GIF from {video_path}")
    
    cap = cv2.VideoCapture(video_path)
    original_fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Calculate frame range
    start_frame = int(start_time * original_fps)
    end_frame = int((start_time + duration) * original_fps)
    frame_step = max(1, original_fps // fps)
    
    # Set start position
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    frames = []
    frame_count = start_frame
    
    while frame_count < end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        
        if (frame_count - start_frame) % frame_step == 0:
            # Resize frame
            h, w = frame.shape[:2]
            new_w = int(w * scale)
            new_h = int(h * scale)
            resized = cv2.resize(frame, (new_w, new_h))
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            frames.append(rgb_frame)
        
        frame_count += 1
    
    cap.release()
    
    if frames:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        imageio.mimsave(output_path, frames, fps=fps)
        print(f"✓ GIF saved: {output_path}")
        print(f"  Frames: {len(frames)} | Duration: {len(frames)/fps:.1f}s")
    else:
        print("No frames extracted for GIF")


def create_screenshot_sequence(
    video_path: str,
    output_dir: str,
    num_screenshots: int = 6,
    interval: str = 'uniform'
):
    """
    Extract screenshots from video.
    
    Args:
        video_path: Path to video file
        output_dir: Directory to save screenshots
        num_screenshots: Number of screenshots to extract
        interval: 'uniform' or 'random'
    """
    print(f"Extracting {num_screenshots} screenshots from {video_path}")
    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Determine frame indices
    if interval == 'uniform':
        frame_indices = np.linspace(0, total_frames - 1, num_screenshots, dtype=int)
    else:
        frame_indices = np.random.randint(0, total_frames, num_screenshots)
        frame_indices.sort()
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for i, frame_idx in enumerate(frame_indices, 1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        
        if ret:
            output_path = Path(output_dir) / f"screenshot_{i:02d}_frame_{frame_idx:05d}.jpg"
            cv2.imwrite(str(output_path), frame)
            print(f"  ✓ Screenshot {i}/{num_screenshots} saved")
    
    cap.release()
    print(f"✓ All screenshots saved to: {output_dir}")


def create_comparison_gif(
    image_paths: list,
    output_path: str,
    duration_per_image: float = 1.0
):
    """
    Create GIF showing before/after comparisons.
    
    Args:
        image_paths: List of image paths to include
        output_path: Path to save GIF
        duration_per_image: Duration to show each image (seconds)
    """
    print(f"Creating comparison GIF with {len(image_paths)} images")
    
    frames = []
    for img_path in image_paths:
        img = cv2.imread(img_path)
        if img is not None:
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frames.append(rgb)
    
    if frames:
        fps = 1 / duration_per_image
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        imageio.mimsave(output_path, frames, fps=fps)
        print(f"✓ Comparison GIF saved: {output_path}")
    else:
        print("No valid images found")


def generate_all_evidence():
    """Generate all evidence materials for documentation."""
    print("="*60)
    print("GENERATING EVIDENCE MATERIALS")
    print("="*60)
    
    # Check if test images exist
    test_images = list(Path("data/input").glob("*.jpg"))
    
    if not test_images:
        print("No test images found. Run download_samples.py first.")
        return
    
    print(f"\nFound {len(test_images)} test images")
    
    # Process images and create GIFs
    results_dir = Path("results/images")
    gifs_dir = Path("results/gifs")
    
    pipeline = DetectionSegmentationPipeline()
    
    processed_images = []
    
    for i, img_path in enumerate(test_images[:3], 1):  # Process first 3 images
        print(f"\n[{i}] Processing {img_path.name}...")
        
        output_path = results_dir / f"evidence_{i}.jpg"
        results = pipeline.process_image(
            str(img_path),
            output_path=str(output_path),
            save_masks=True,
            save_json=True
        )
        
        processed_images.append(str(output_path))
        print(f"  ✓ Processed: {results['num_detections']} detections")
    
    # Create comparison GIF
    if processed_images:
        print("\nCreating comparison GIF...")
        create_comparison_gif(
            processed_images,
            str(gifs_dir / "detection_comparison.gif"),
            duration_per_image=2.0
        )
    
    # Generate GIFs from results
    print("\nCreating demo GIFs...")
    
    # GIF 1: Detection process
    print("\nNote: For video GIFs, you need to process a video first.")
    print("Run: python python/detection/video_processor.py --source <video> --output results/videos/demo.mp4")
    
    print("\n" + "="*60)
    print("EVIDENCE GENERATION COMPLETE!")
    print("="*60)
    print("\nGenerated:")
    print(f"  - {len(processed_images)} processed images")
    print(f"  - 1 comparison GIF")
    print("\nTo generate video GIFs:")
    print("  1. Process a video file or record from webcam")
    print("  2. Run this script with video paths")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate evidence materials")
    parser.add_argument('--mode', choices=['all', 'video', 'gif', 'screenshots'], 
                       default='all', help='Generation mode')
    parser.add_argument('--video', type=str, help='Video file path')
    parser.add_argument('--output', type=str, help='Output path')
    
    args = parser.parse_args()
    
    if args.mode == 'all':
        generate_all_evidence()
    
    elif args.mode == 'video' and args.video:
        create_demo_video(
            args.video,
            args.output or 'results/videos/demo.mp4',
            duration=30
        )
    
    elif args.mode == 'gif' and args.video:
        video_to_gif(
            args.video,
            args.output or 'results/gifs/demo.gif',
            start_time=0,
            duration=5,
            fps=10
        )
    
    elif args.mode == 'screenshots' and args.video:
        create_screenshot_sequence(
            args.video,
            args.output or 'results/images/screenshots',
            num_screenshots=6
        )


if __name__ == "__main__":
    main()
