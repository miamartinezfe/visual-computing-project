# -*- coding: utf-8 -*-
"""
Práctica de Percepción Multimodal - Punto 4: SAM - Segmentación por Prompts
Este script implementa detección de objetos con YOLO, segmentación con SAM usando bounding boxes y puntos,
y evaluación comparativa mediante métricas IoU.
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
from segment_anything import SamPredictor, sam_model_registry
from skimage.metrics import structural_similarity as compare_ssim
from skimage.transform import resize # Import resize function

# Función para cargar imágenes
def load_images(image_dir):
    """Carga todas las imágenes de un directorio."""
    images = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Se encontraron {len(images)} imágenes en el directorio.")
    return images

# Función para detección con YOLO
def detect_objects(model, image_dir):
    """Realiza detección de objetos en las imágenes del directorio."""
    results = model.predict(source=image_dir, save=False)
    return results

# Función para validar entradas
def validate_inputs(images, bboxes):
    """Valida que las imágenes y bounding boxes no estén vacíos."""
    if not images:
        raise ValueError("No se encontraron imágenes para procesar.")
    if bboxes is None or len(bboxes) == 0:
        raise ValueError("No se encontraron bounding boxes para procesar.")

# Función para guardar máscaras
def save_masks(masks, image_name, output_dir="results/masks"):
    """Guarda las máscaras binarias generadas en formato PNG."""
    os.makedirs(output_dir, exist_ok=True)
    for i, mask in enumerate(masks):
        mask_path = os.path.join(output_dir, f"{image_name}_mask_{i}.png")
        cv2.imwrite(mask_path, (mask * 255).astype(np.uint8))

# Función para segmentación con SAM usando bounding boxes
def segment_with_sam_bboxes(image, bboxes, predictor):
    """Genera máscaras binarias usando bounding boxes como prompts."""
    masks_output = []
    predictor.set_image(image)
    if bboxes.shape[0] > 0:
        for bbox in bboxes:
            input_box = np.array([bbox])
            masks, _, _ = predictor.predict(box=input_box, multimask_output=False)
            # Ensure mask is boolean and has the same dimensions as the original image
            # The predict method often returns masks of the image size, but let's be explicit
            if masks.shape[-2:] != image.shape[:2]:
                mask_resized = resize(masks[0], image.shape[:2], anti_aliasing=True) > 0.5 # Resize and binarize
                masks_output.append(mask_resized)
            else:
                masks_output.append(masks[0] > 0) # Ensure boolean mask
    # Guardar máscaras generadas
    save_masks(masks_output, "image_name_placeholder")  # Reemplazar con el nombre real de la imagen
    return masks_output

# Función para segmentación con SAM usando puntos
def segment_with_sam_points(image, points, predictor):
    """Genera máscaras binarias usando puntos como prompts."""
    predictor.set_image(image)
    # Ensure points are in the correct format (N, 2)
    if points.ndim == 1:
        points = np.array([points]) # Make sure it's (N, 2)
    if points.shape[1] != 2:
        raise ValueError("Los puntos deben estar en formato (N, 2).")

    masks, _, _ = predictor.predict(point_coords=points, point_labels=np.ones(points.shape[0]), multimask_output=False)
    # Ensure mask is boolean and has the same dimensions as the original image
    if masks.shape[-2:] != image.shape[:2]:
        mask_resized = resize(masks[0], image.shape[:2], anti_aliasing=True) > 0.5 # Resize and binarize
        return mask_resized
    else:
        return masks[0] > 0 # Ensure boolean mask


# Función para calcular IoU
def calculate_iou(mask1, mask2):
    """Calcula la métrica IoU entre dos máscaras binarias, redimensionando si es necesario."""
    # Ensure masks have the same shape
    if mask1.shape != mask2.shape:
        # Resize mask1 to match mask2's shape
        mask1_resized = resize(mask1, mask2.shape, anti_aliasing=True) > 0.5
        mask1 = mask1_resized

    intersection = np.logical_and(mask1, mask2)
    union = np.logical_or(mask1, mask2)
    # Avoid division by zero if union is empty
    if np.sum(union) == 0:
        return 0.0
    iou = np.sum(intersection) / np.sum(union)
    return iou

# Function to combine multiple masks into a single mask
def combine_masks(masks):
    """Combines a list of binary masks into a single mask using logical OR."""
    if not masks:
        return None # Return None if the list is empty
    combined_mask = np.logical_or.reduce(masks)
    return combined_mask

# Función para guardar visualizaciones comparativas
def save_comparative_visualization(img, combined_mask_bbox, combined_mask_points, output_path):
    """Genera y guarda una visualización comparativa de las máscaras."""
    plt.figure(figsize=(15, 5)) # Adjust figure size for better visualization
    plt.subplot(1, 3, 1)
    plt.title("Imagen Original")
    plt.imshow(img)
    plt.axis('off')

    plt.subplot(1, 3, 2) # Changed back to 3 columns
    plt.title("Segmentación Bounding Box") # Separate title
    plt.imshow(img) # Display the original image
    if combined_mask_bbox is not None:
        # Overlay bounding box mask with a color
        mask_bbox_colored = np.zeros((combined_mask_bbox.shape[0], combined_mask_bbox.shape[1], 3), dtype=np.uint8)
        mask_bbox_colored[combined_mask_bbox] = [255, 0, 0] # Red for bbox mask
        plt.imshow(mask_bbox_colored, alpha=0.5) # Removed cmap for colored overlay

    plt.subplot(1, 3, 3) # Added the third subplot
    plt.title("Segmentación Puntos") # Separate title
    plt.imshow(img) # Display the original image
    if combined_mask_points is not None:
        # Overlay points mask with a different color
        mask_points_colored = np.zeros((combined_mask_points.shape[0], combined_mask_points.shape[1], 3), dtype=np.uint8)
        mask_points_colored[combined_mask_points] = [0, 0, 255] # Blue for points mask
        plt.imshow(mask_points_colored, alpha=0.5) # Removed cmap for colored overlay

    plt.axis('off')

    plt.tight_layout() # Adjust layout to prevent overlap
    plt.savefig(output_path)
    plt.close()

# Configuración inicial
if __name__ == "__main__":
    # Directorios
    image_dir = "data"
    output_dir = "results/comparativas"
    os.makedirs(output_dir, exist_ok=True)

    # Cargar imágenes
    images_paths = load_images(image_dir)

    # Modelo YOLO
    model = YOLO("yolov8n.pt")
    results = detect_objects(model, image_dir)

    # Modelo SAM
    sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b_01ec64.pth")
    predictor = SamPredictor(sam)

    # Segmentación y evaluación
    all_iou_scores = {} # Dictionary to store IoU scores per image and object

    for i, result in enumerate(results): # Iterate through YOLO results
        img_path = result.path
        img_name = os.path.basename(img_path)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Extract bounding boxes for the current image
        image_bboxes = result.boxes.xyxy.cpu().numpy()

        masks_bboxes = []
        masks_points = []
        iou_scores_per_image = []

        if image_bboxes.shape[0] > 0:
            # Segmentación con bounding boxes for the current image
            masks_bboxes = segment_with_sam_bboxes(img, image_bboxes, predictor)

            # Segmentación con puntos (example using a point for each detected object's center)
            points = []
            for bbox in image_bboxes:
                x1, y1, x2, y2 = bbox
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                points.append([center_x, center_y])
            points = np.array(points)


            if points.shape[0] > 0:
                # Generate a point-based mask for each point individually
                for point in points:
                    mask_points = segment_with_sam_points(img, point, predictor)
                    masks_points.append(mask_points)


            # Comparativa y cálculo de IoU
            # Assuming masks_bboxes and masks_points are paired by object
            min_masks = min(len(masks_bboxes), len(masks_points))
            for j in range(min_masks):
                iou = calculate_iou(masks_bboxes[j], masks_points[j])
                print(f"Image: {img_name}, Object {j+1}: IoU between bounding box and point mask: {iou}")
                iou_scores_per_image.append(iou)

            # Store IoU scores
            all_iou_scores[img_name] = iou_scores_per_image

            # Combine masks for visualization
            combined_mask_bbox = combine_masks(masks_bboxes)
            combined_mask_points = combine_masks(masks_points)

            # Save comparative visualization once per image
            if combined_mask_bbox is not None or combined_mask_points is not None:
                output_path = os.path.join(output_dir, f"comparativa_{img_name}")
                save_comparative_visualization(img, combined_mask_bbox, combined_mask_points, output_path)
            else:
                print(f"No masks generated for {img_name} to save comparative visualization.")

        else:
            print(f"No objects detected by YOLO in {img_path}. Skipping segmentation and IoU calculation.")

    print("\n--- IoU Scores Summary ---")
    for img_name, iou_scores in all_iou_scores.items():
        print(f"Image: {img_name}")
        if iou_scores:
            for j, iou in enumerate(iou_scores):
                print(f"  Object {j+1}: IoU = {iou:.4f}")
        else:
            print("  No IoU scores calculated.")
    print("--------------------------")

    print("Proceso completado. Visualizaciones guardadas en 'results/comparativas'.")