"""
Visualization utilities for detection and segmentation results.
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import pandas as pd


def create_comparison_image(
    images: List[np.ndarray],
    titles: List[str],
    output_path: Optional[str] = None
) -> np.ndarray:
    """
    Create side-by-side comparison of images.
    
    Args:
        images: List of images to compare
        titles: List of titles for each image
        output_path: Optional path to save image
        
    Returns:
        Combined comparison image
    """
    n = len(images)
    fig, axes = plt.subplots(1, n, figsize=(5*n, 5))
    
    if n == 1:
        axes = [axes]
    
    for i, (img, title) in enumerate(zip(images, titles)):
        # Convert BGR to RGB for matplotlib
        if len(img.shape) == 3:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = img
        
        axes[i].imshow(img_rgb)
        axes[i].set_title(title, fontsize=14)
        axes[i].axis('off')
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        print(f"Comparison saved to: {output_path}")
    
    # Convert to numpy array
    fig.canvas.draw()
    comparison = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    comparison = comparison.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    
    plt.close()
    
    return comparison


def plot_metrics_timeline(
    csv_path: str,
    output_path: Optional[str] = None
):
    """
    Plot metrics over time.
    
    Args:
        csv_path: Path to metrics CSV file
        output_path: Path to save plot
    """
    df = pd.read_csv(csv_path)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # FPS over time
    axes[0, 0].plot(df['frame'], df['fps'], linewidth=2, color='blue')
    axes[0, 0].set_title('FPS over Time', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Frame')
    axes[0, 0].set_ylabel('FPS')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Detections over time
    axes[0, 1].plot(df['frame'], df['detections'], linewidth=2, color='green')
    axes[0, 1].set_title('Detections over Time', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Frame')
    axes[0, 1].set_ylabel('Number of Detections')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Processing time breakdown
    axes[1, 0].plot(df['frame'], df['detection_time_ms'], label='Detection', linewidth=2)
    axes[1, 0].plot(df['frame'], df['segmentation_time_ms'], label='Segmentation', linewidth=2)
    axes[1, 0].plot(df['frame'], df['total_time_ms'], label='Total', linewidth=2, linestyle='--')
    axes[1, 0].set_title('Processing Time Breakdown', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Frame')
    axes[1, 0].set_ylabel('Time (ms)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Resource usage
    axes[1, 1].plot(df['frame'], df['cpu_percent'], label='CPU %', linewidth=2)
    axes[1, 1].plot(df['frame'], df['ram_percent'], label='RAM %', linewidth=2)
    axes[1, 1].set_title('Resource Usage', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Frame')
    axes[1, 1].set_ylabel('Usage (%)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        print(f"Metrics plot saved to: {output_path}")
    
    plt.close()


def create_detection_grid(
    detections: List[Dict],
    image: np.ndarray,
    output_path: Optional[str] = None,
    grid_size: Tuple[int, int] = (3, 3)
) -> np.ndarray:
    """
    Create a grid of detected objects.
    
    Args:
        detections: List of detections with bbox
        image: Original image
        output_path: Path to save grid
        grid_size: Grid dimensions (rows, cols)
        
    Returns:
        Grid image
    """
    rows, cols = grid_size
    max_objects = rows * cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(3*cols, 3*rows))
    axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]
    
    for i in range(max_objects):
        if i < len(detections):
            det = detections[i]
            x1, y1, x2, y2 = det['bbox']
            
            # Crop object
            obj_img = image[y1:y2, x1:x2]
            
            # Convert BGR to RGB
            obj_rgb = cv2.cvtColor(obj_img, cv2.COLOR_BGR2RGB)
            
            axes[i].imshow(obj_rgb)
            axes[i].set_title(
                f"{det['class_name']}\n{det['confidence']:.2f}",
                fontsize=10
            )
        else:
            axes[i].axis('off')
        
        axes[i].set_xticks([])
        axes[i].set_yticks([])
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        print(f"Detection grid saved to: {output_path}")
    
    plt.close()


def annotate_image_advanced(
    image: np.ndarray,
    detections: List[Dict],
    show_masks: bool = True,
    show_labels: bool = True,
    show_confidence: bool = True,
    mask_alpha: float = 0.4
) -> np.ndarray:
    """
    Advanced annotation with customization options.
    
    Args:
        image: Input image
        detections: List of detections
        show_masks: Show segmentation masks
        show_labels: Show class labels
        show_confidence: Show confidence scores
        mask_alpha: Mask transparency
        
    Returns:
        Annotated image
    """
    result = image.copy()
    
    for i, det in enumerate(detections):
        x1, y1, x2, y2 = det['bbox']
        
        # Generate color
        np.random.seed(i)
        color = tuple(map(int, np.random.randint(50, 255, 3)))
        
        # Draw mask if available
        if show_masks and 'mask' in det:
            mask = det['mask']
            colored_mask = np.zeros_like(image)
            colored_mask[mask] = color
            result = cv2.addWeighted(result, 1, colored_mask, mask_alpha, 0)
        
        # Draw bounding box
        cv2.rectangle(result, (x1, y1), (x2, y2), color, 2)
        
        # Draw label
        if show_labels or show_confidence:
            label_parts = []
            if show_labels:
                label_parts.append(det['class_name'])
            if show_confidence:
                label_parts.append(f"{det['confidence']:.2f}")
            
            label = " ".join(label_parts)
            
            # Label background
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(result, (x1, y1 - th - 10), (x1 + tw, y1), color, -1)
            
            # Label text
            cv2.putText(
                result, label, (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255, 255, 255), 1
            )
    
    return result
