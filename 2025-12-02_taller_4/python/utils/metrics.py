"""
Metrics and Performance Monitoring
Track FPS, latency, resource usage, and other metrics.
"""
import time
import psutil
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import json

try:
    import torch
except ImportError:
    torch = None


class MetricsTracker:
    """Track and log performance metrics."""
    
    def __init__(self):
        """Initialize metrics tracker."""
        self.metrics = []
        self.start_time = time.time()
        self.process = psutil.Process()
    
    def record_frame(
        self,
        frame_num: int,
        num_detections: int,
        detection_time: float,
        segmentation_time: float,
        total_time: float
    ):
        """
        Record metrics for a single frame.
        
        Args:
            frame_num: Frame number
            num_detections: Number of objects detected
            detection_time: Time spent on detection (seconds)
            segmentation_time: Time spent on segmentation (seconds)
            total_time: Total processing time (seconds)
        """
        # Calculate metrics
        fps = 1 / total_time if total_time > 0 else 0
        
        # Get resource usage
        cpu_percent = self.process.cpu_percent()
        memory_mb = self.process.memory_info().rss / 1024 / 1024
        
        # GPU usage (if available)
        gpu_memory_mb = 0
        gpu_utilization = 0
        
        if torch and torch.cuda.is_available():
            gpu_memory_mb = torch.cuda.memory_allocated() / 1024 / 1024
            # Note: GPU utilization requires nvidia-ml-py3 for accurate readings
        
        metric = {
            'timestamp': time.time(),
            'frame_num': frame_num,
            'num_detections': num_detections,
            'detection_time_ms': detection_time * 1000,
            'segmentation_time_ms': segmentation_time * 1000,
            'total_time_ms': total_time * 1000,
            'fps': fps,
            'cpu_percent': cpu_percent,
            'memory_mb': memory_mb,
            'gpu_memory_mb': gpu_memory_mb,
            'gpu_utilization': gpu_utilization
        }
        
        self.metrics.append(metric)
    
    def get_summary(self) -> Dict:
        """
        Get summary statistics.
        
        Returns:
            Dictionary with aggregated metrics
        """
        if not self.metrics:
            return {}
        
        df = pd.DataFrame(self.metrics)
        
        summary = {
            'total_frames': len(self.metrics),
            'total_detections': df['num_detections'].sum(),
            'avg_detections_per_frame': df['num_detections'].mean(),
            'avg_detection_time_ms': df['detection_time_ms'].mean(),
            'avg_segmentation_time_ms': df['segmentation_time_ms'].mean(),
            'avg_total_time_ms': df['total_time_ms'].mean(),
            'avg_fps': df['fps'].mean(),
            'max_fps': df['fps'].max(),
            'min_fps': df['fps'].min(),
            'avg_cpu_percent': df['cpu_percent'].mean(),
            'avg_memory_mb': df['memory_mb'].mean(),
            'max_memory_mb': df['memory_mb'].max(),
            'avg_gpu_memory_mb': df['gpu_memory_mb'].mean(),
            'max_gpu_memory_mb': df['gpu_memory_mb'].max(),
            'total_duration_s': time.time() - self.start_time
        }
        
        return summary
    
    def save_csv(self, output_path: str):
        """
        Save metrics to CSV file.
        
        Args:
            output_path: Path to save CSV
        """
        if not self.metrics:
            print("No metrics to save")
            return
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(self.metrics)
        df.to_csv(output_path, index=False)
        
        print(f"Metrics saved to: {output_path}")
    
    def save_json(self, output_path: str):
        """
        Save metrics summary to JSON.
        
        Args:
            output_path: Path to save JSON
        """
        summary = self.get_summary()
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Summary saved to: {output_path}")
    
    def print_summary(self):
        """Print summary statistics to console."""
        summary = self.get_summary()
        
        if not summary:
            print("No metrics recorded")
            return
        
        print("\n" + "=" * 60)
        print("PERFORMANCE METRICS SUMMARY")
        print("=" * 60)
        print(f"Total frames: {summary['total_frames']}")
        print(f"Total detections: {summary['total_detections']}")
        print(f"Avg detections/frame: {summary['avg_detections_per_frame']:.2f}")
        print("\nTiming:")
        print(f"  Avg detection time: {summary['avg_detection_time_ms']:.2f} ms")
        print(f"  Avg segmentation time: {summary['avg_segmentation_time_ms']:.2f} ms")
        print(f"  Avg total time: {summary['avg_total_time_ms']:.2f} ms")
        print(f"  Avg FPS: {summary['avg_fps']:.2f}")
        print(f"  Max FPS: {summary['max_fps']:.2f}")
        print(f"  Min FPS: {summary['min_fps']:.2f}")
        print("\nResources:")
        print(f"  Avg CPU: {summary['avg_cpu_percent']:.1f}%")
        print(f"  Avg RAM: {summary['avg_memory_mb']:.1f} MB")
        print(f"  Max RAM: {summary['max_memory_mb']:.1f} MB")
        if summary['avg_gpu_memory_mb'] > 0:
            print(f"  Avg GPU memory: {summary['avg_gpu_memory_mb']:.1f} MB")
            print(f"  Max GPU memory: {summary['max_gpu_memory_mb']:.1f} MB")
        print("\nDuration:")
        print(f"  Total: {summary['total_duration_s']:.2f} seconds")
        print("=" * 60)


class BenchmarkRunner:
    """Run benchmarks on models."""
    
    @staticmethod
    def benchmark_yolo(
        model,
        image,
        num_runs: int = 100,
        warmup_runs: int = 10
    ) -> Dict:
        """
        Benchmark YOLO detection speed.
        
        Args:
            model: YOLO detector instance
            image: Test image
            num_runs: Number of benchmark runs
            warmup_runs: Number of warmup runs
            
        Returns:
            Benchmark results
        """
        print(f"\nBenchmarking YOLO ({num_runs} runs)...")
        
        # Warmup
        for _ in range(warmup_runs):
            model.detect(image)
        
        # Benchmark
        times = []
        for i in range(num_runs):
            start = time.time()
            detections, _ = model.detect(image)
            elapsed = time.time() - start
            times.append(elapsed)
            
            if (i + 1) % 20 == 0:
                print(f"  Progress: {i + 1}/{num_runs}")
        
        results = {
            'model': 'YOLO',
            'num_runs': num_runs,
            'avg_time_ms': (sum(times) / len(times)) * 1000,
            'min_time_ms': min(times) * 1000,
            'max_time_ms': max(times) * 1000,
            'avg_fps': 1 / (sum(times) / len(times)),
            'max_fps': 1 / min(times)
        }
        
        print(f"  Avg time: {results['avg_time_ms']:.2f} ms")
        print(f"  Avg FPS: {results['avg_fps']:.2f}")
        
        return results
    
    @staticmethod
    def benchmark_sam(
        model,
        image,
        bbox,
        num_runs: int = 50,
        warmup_runs: int = 5
    ) -> Dict:
        """
        Benchmark SAM segmentation speed.
        
        Args:
            model: SAM segmenter instance
            image: Test image
            bbox: Bounding box for segmentation
            num_runs: Number of benchmark runs
            warmup_runs: Number of warmup runs
            
        Returns:
            Benchmark results
        """
        print(f"\nBenchmarking SAM ({num_runs} runs)...")
        
        # Set image once
        import cv2
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        model.set_image(rgb_image)
        
        # Warmup
        for _ in range(warmup_runs):
            model.segment_from_bbox(bbox)
        
        # Benchmark
        times = []
        for i in range(num_runs):
            start = time.time()
            mask, score, _ = model.segment_from_bbox(bbox)
            elapsed = time.time() - start
            times.append(elapsed)
            
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i + 1}/{num_runs}")
        
        results = {
            'model': 'SAM',
            'num_runs': num_runs,
            'avg_time_ms': (sum(times) / len(times)) * 1000,
            'min_time_ms': min(times) * 1000,
            'max_time_ms': max(times) * 1000,
            'avg_fps': 1 / (sum(times) / len(times)),
            'max_fps': 1 / min(times)
        }
        
        print(f"  Avg time: {results['avg_time_ms']:.2f} ms")
        print(f"  Avg FPS: {results['avg_fps']:.2f}")
        
        return results


def main():
    """Demo metrics tracking."""
    tracker = MetricsTracker()
    
    # Simulate some frames
    import random
    for i in range(100):
        num_dets = random.randint(0, 10)
        det_time = random.uniform(0.01, 0.05)
        seg_time = random.uniform(0.005, 0.02) * num_dets
        total = det_time + seg_time
        
        tracker.record_frame(i, num_dets, det_time, seg_time, total)
    
    # Print summary
    tracker.print_summary()
    
    # Save metrics
    tracker.save_csv("results/metrics/demo_metrics.csv")
    tracker.save_json("results/metrics/demo_summary.json")


if __name__ == "__main__":
    main()
