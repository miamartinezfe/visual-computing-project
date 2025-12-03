"""
SAM (Segment Anything Model) Segmenter
Handles semantic segmentation using Meta's SAM model.
"""
import cv2
import numpy as np
import torch
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from segment_anything import sam_model_registry, SamPredictor
import time


class SAMSegmenter:
    """
    Segment Anything Model for precise segmentation.
    """
    
    def __init__(
        self,
        model_type: str = "vit_b",
        checkpoint_path: str = "data/models/sam_vit_b_01ec64.pth",
        device: str = "cuda"
    ):
        """
        Initialize SAM segmenter.
        
        Args:
            model_type: Type of SAM model ('vit_h', 'vit_l', or 'vit_b')
            checkpoint_path: Path to SAM checkpoint
            device: Device to run inference on ('cuda' or 'cpu')
        """
        self.model_type = model_type
        self.checkpoint_path = checkpoint_path
        self.device = device
        
        print(f"Loading SAM model: {model_type}")
        
        if not Path(checkpoint_path).exists():
            raise FileNotFoundError(
                f"SAM checkpoint not found: {checkpoint_path}\n"
                "Please run download_models.py first."
            )
        
        # Load SAM model
        self.sam = sam_model_registry[model_type](checkpoint=checkpoint_path)
        self.sam.to(device=device)
        
        # Create predictor
        self.predictor = SamPredictor(self.sam)
        
        print(f"✓ SAM model loaded on {device}")
    
    def set_image(self, image: np.ndarray):
        """
        Set the image for segmentation (preprocessing).
        
        Args:
            image: Input image in RGB format
        """
        self.predictor.set_image(image)
    
    def segment_from_bbox(
        self,
        bbox: List[int],
        image: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, float]:
        """
        Generate segmentation mask from bounding box.
        
        Args:
            bbox: Bounding box [x1, y1, x2, y2]
            image: Input image (if not already set)
            
        Returns:
            mask: Binary segmentation mask
            score: Confidence score
        """
        start_time = time.time()
        
        # Set image if provided
        if image is not None:
            self.set_image(image)
        
        # Convert bbox to SAM input format
        x1, y1, x2, y2 = bbox
        input_box = np.array([x1, y1, x2, y2])
        
        # Predict mask
        masks, scores, logits = self.predictor.predict(
            box=input_box,
            multimask_output=False
        )
        
        inference_time = time.time() - start_time
        
        # Return best mask
        mask = masks[0]
        score = float(scores[0])
        
        return mask, score, inference_time
    
    def segment_from_points(
        self,
        points: np.ndarray,
        labels: np.ndarray,
        image: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, float]:
        """
        Generate segmentation mask from point prompts.
        
        Args:
            points: Array of points [[x1, y1], [x2, y2], ...]
            labels: Array of labels (1=foreground, 0=background)
            image: Input image (if not already set)
            
        Returns:
            mask: Binary segmentation mask
            score: Confidence score
        """
        start_time = time.time()
        
        if image is not None:
            self.set_image(image)
        
        # Predict mask
        masks, scores, logits = self.predictor.predict(
            point_coords=points,
            point_labels=labels,
            multimask_output=False
        )
        
        inference_time = time.time() - start_time
        
        mask = masks[0]
        score = float(scores[0])
        
        return mask, score, inference_time
    
    def segment_detections(
        self,
        image: np.ndarray,
        detections: List[Dict]
    ) -> List[Dict]:
        """
        Generate segmentation masks for all detections.
        
        Args:
            image: Input image (RGB)
            detections: List of detection dictionaries with 'bbox' key
            
        Returns:
            List of detections with added 'mask' and 'seg_score' keys
        """
        # Preprocess image once
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.set_image(rgb_image)
        
        total_time = 0
        
        for detection in detections:
            bbox = detection['bbox']
            mask, score, inference_time = self.segment_from_bbox(bbox)
            
            detection['mask'] = mask
            detection['seg_score'] = score
            total_time += inference_time
        
        avg_time = total_time / len(detections) if detections else 0
        
        return detections, avg_time
    
    def visualize_mask(
        self,
        image: np.ndarray,
        mask: np.ndarray,
        color: Tuple[int, int, int] = (0, 255, 0),
        alpha: float = 0.5
    ) -> np.ndarray:
        """
        Overlay segmentation mask on image.
        
        Args:
            image: Input image
            mask: Binary mask
            color: RGB color for mask
            alpha: Transparency (0=transparent, 1=opaque)
            
        Returns:
            Image with mask overlay
        """
        overlay = image.copy()
        
        # Create colored mask
        colored_mask = np.zeros_like(image)
        colored_mask[mask] = color
        
        # Blend with original image
        result = cv2.addWeighted(overlay, 1 - alpha, colored_mask, alpha, 0)
        
        return result
    
    def visualize_detections_with_masks(
        self,
        image: np.ndarray,
        detections: List[Dict],
        alpha: float = 0.5
    ) -> np.ndarray:
        """
        Visualize all detections with segmentation masks.
        
        Args:
            image: Input image
            detections: List of detections with 'mask' key
            alpha: Mask transparency
            
        Returns:
            Annotated image
        """
        result = image.copy()
        
        for i, det in enumerate(detections):
            if 'mask' not in det:
                continue
            
            mask = det['mask']
            
            # Generate unique color per detection
            np.random.seed(i)
            color = tuple(map(int, np.random.randint(50, 255, 3)))
            
            # Apply mask
            colored_mask = np.zeros_like(image)
            colored_mask[mask] = color
            result = cv2.addWeighted(result, 1, colored_mask, alpha, 0)
            
            # Draw contours
            contours, _ = cv2.findContours(
                mask.astype(np.uint8),
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            cv2.drawContours(result, contours, -1, color, 2)
        
        return result
    
    def save_masks(
        self,
        detections: List[Dict],
        output_dir: str
    ):
        """
        Save individual masks to files.
        
        Args:
            detections: List of detections with masks
            output_dir: Directory to save masks
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for i, det in enumerate(detections):
            if 'mask' not in det:
                continue
            
            mask = det['mask'].astype(np.uint8) * 255
            class_name = det.get('class_name', 'unknown')
            
            filename = f"mask_{i:03d}_{class_name}.png"
            cv2.imwrite(str(output_path / filename), mask)
        
        print(f"Saved {len(detections)} masks to {output_dir}")


def main():
    """Demo usage of SAMSegmenter."""
    from yolo_detector import YOLODetector
    
    # Initialize models
    print("Initializing YOLO detector...")
    detector = YOLODetector(model_path="yolov8n.pt", device="cuda")
    
    print("\nInitializing SAM segmenter...")
    segmenter = SAMSegmenter(
        model_type="vit_b",
        checkpoint_path="data/models/sam_vit_b_01ec64.pth",
        device="cuda"
    )
    
    # Test with sample image
    test_image_path = "data/input/test.jpg"
    
    if Path(test_image_path).exists():
        print(f"\nProcessing: {test_image_path}")
        
        # Load image
        image = cv2.imread(test_image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect objects
        print("Detecting objects...")
        detections, det_time = detector.detect(image)
        print(f"Found {len(detections)} objects in {det_time*1000:.2f} ms")
        
        # Segment detections
        print("Segmenting objects...")
        detections_with_masks, seg_time = segmenter.segment_detections(
            image, detections
        )
        print(f"Segmented in {seg_time*1000:.2f} ms/object")
        
        # Visualize results
        result = segmenter.visualize_detections_with_masks(
            image, detections_with_masks, alpha=0.5
        )
        
        # Save output
        output_path = "results/images/sam_test_output.jpg"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(output_path, result)
        print(f"\nSaved: {output_path}")
        
        # Save individual masks
        segmenter.save_masks(detections_with_masks, "results/images/masks")
        
    else:
        print(f"No test image found at {test_image_path}")
        print("Please add a test image and run again.")


if __name__ == "__main__":
    main()
