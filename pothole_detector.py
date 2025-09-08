import cv2
import numpy as np
import tensorflow as tf
from typing import Dict, List, Tuple
import os

class PotholeDetector:
    """
    A free, custom pothole detection model using computer vision techniques
    and transfer learning with a pre-trained model.
    """
    
    def __init__(self):
        self.model = None
        self.loaded = False
        self.confidence_threshold = 0.5
        self.load_model()
    
    def load_model(self):
        """
        Load or create the pothole detection model.
        Uses a combination of traditional CV and simple ML for free implementation.
        """
        try:
            # For now, we'll use a rule-based approach with computer vision
            # This can be enhanced with a trained model later
            self.loaded = True
            print("Pothole detector initialized successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.loaded = False
    
    def is_loaded(self) -> bool:
        """Check if the model is loaded"""
        return self.loaded
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess the image for pothole detection
        """
        # Resize image to standard size
        height, width = image.shape[:2]
        if width > 800:
            scale = 800 / width
            new_width = 800
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height))
        
        return image
    
    def detect_dark_regions(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect dark regions that might be potholes using computer vision
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding to find dark regions
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                     cv2.THRESH_BINARY_INV, 11, 2)
        
        # Morphological operations to clean up the image
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area and aspect ratio
        potential_potholes = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 100 or area > 50000:  # Filter by size
                continue
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            
            # Potholes are generally somewhat circular or irregular
            if 0.3 < aspect_ratio < 3.0:
                potential_potholes.append((x, y, w, h))
        
        return potential_potholes
    
    def detect_edge_features(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect potholes using edge detection and contour analysis
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Canny edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Dilate edges to connect nearby edges
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        potential_potholes = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 200 or area > 30000:
                continue
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Check if the region looks like a pothole
            roi = gray[y:y+h, x:x+w]
            if roi.size > 0:
                mean_intensity = np.mean(roi)
                # Potholes are typically darker than surrounding road
                if mean_intensity < np.mean(gray) * 0.8:
                    potential_potholes.append((x, y, w, h))
        
        return potential_potholes
    
    def combine_detections(self, detections1: List, detections2: List) -> List:
        """
        Combine detections from multiple methods and remove duplicates
        """
        all_detections = detections1 + detections2
        
        # Simple non-maximum suppression
        final_detections = []
        for i, (x1, y1, w1, h1) in enumerate(all_detections):
            is_duplicate = False
            for j, (x2, y2, w2, h2) in enumerate(final_detections):
                # Calculate overlap
                overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
                overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
                overlap_area = overlap_x * overlap_y
                
                area1 = w1 * h1
                area2 = w2 * h2
                
                # If significant overlap, consider it duplicate
                if overlap_area > 0.3 * min(area1, area2):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                final_detections.append((x1, y1, w1, h1))
        
        return final_detections
    
    def detect(self, image: np.ndarray) -> Dict:
        """
        Main detection method that combines multiple approaches
        """
        if not self.loaded:
            return {"count": 0, "boxes": [], "confidences": []}
        
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        # Apply multiple detection methods
        dark_regions = self.detect_dark_regions(processed_image)
        edge_features = self.detect_edge_features(processed_image)
        
        # Combine detections
        final_detections = self.combine_detections(dark_regions, edge_features)
        
        # Generate confidence scores (simplified for this implementation)
        confidences = []
        for box in final_detections:
            x, y, w, h = box
            roi = cv2.cvtColor(processed_image[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
            
            # Simple confidence based on darkness and size
            if roi.size > 0:
                darkness_score = 1.0 - (np.mean(roi) / 255.0)
                size_score = min(1.0, (w * h) / 1000.0)
                confidence = min(0.95, (darkness_score + size_score) / 2.0)
                confidences.append(max(0.1, confidence))
            else:
                confidences.append(0.1)
        
        return {
            "count": len(final_detections),
            "boxes": final_detections,
            "confidences": confidences
        }