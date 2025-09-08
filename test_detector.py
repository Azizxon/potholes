#!/usr/bin/env python3
"""
Test script for the pothole detection system
"""

import os
import sys
import numpy as np
import cv2
from PIL import Image
from pothole_detector import PotholeDetector

def create_test_image():
    """Create a simple test image with dark spots that could be potholes"""
    # Create a gray road-like image
    img = np.ones((400, 600, 3), dtype=np.uint8) * 120  # Gray road
    
    # Add some dark circular spots (simulated potholes)
    cv2.circle(img, (150, 200), 30, (40, 40, 40), -1)  # Dark spot 1
    cv2.circle(img, (450, 150), 25, (30, 30, 30), -1)  # Dark spot 2
    
    # Add some noise and texture
    noise = np.random.randint(0, 20, img.shape, dtype=np.uint8)
    img = cv2.add(img, noise)
    
    return img

def test_detector():
    """Test the pothole detector with a synthetic image"""
    print("🧪 Testing Pothole Detection System")
    print("=" * 40)
    
    # Initialize detector
    print("1. Initializing detector...")
    detector = PotholeDetector()
    
    if not detector.is_loaded():
        print("❌ Detector failed to load!")
        return False
    
    print("✅ Detector loaded successfully")
    
    # Create test image
    print("2. Creating test image...")
    test_image = create_test_image()
    
    # Save test image for reference
    cv2.imwrite("test_road.jpg", test_image)
    print("✅ Test image saved as test_road.jpg")
    
    # Run detection
    print("3. Running detection...")
    results = detector.detect(test_image)
    
    print(f"✅ Detection complete!")
    print(f"   Potholes detected: {results['count']}")
    print(f"   Confidence scores: {[f'{c:.2f}' for c in results['confidences']]}")
    print(f"   Bounding boxes: {results['boxes']}")
    
    # Draw results on image
    if results['count'] > 0:
        result_image = test_image.copy()
        for i, (x, y, w, h) in enumerate(results['boxes']):
            cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(result_image, f"Pothole {i+1}", (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        cv2.imwrite("test_road_result.jpg", result_image)
        print("✅ Result image saved as test_road_result.jpg")
    
    print("\n🎉 Test completed successfully!")
    return True

def test_api_health():
    """Test if the API components can be imported"""
    print("4. Testing API components...")
    try:
        from app import app
        print("✅ FastAPI app can be imported")
        return True
    except Exception as e:
        print(f"❌ Error importing API: {e}")
        return False

if __name__ == "__main__":
    success = test_detector()
    api_success = test_api_health()
    
    if success and api_success:
        print("\n🌟 All tests passed! The system is ready to use.")
        print("\nTo run the web interface:")
        print("  python app.py")
        print("\nThen open http://localhost:8000 in your browser")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        sys.exit(1)