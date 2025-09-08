from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import cv2
import numpy as np
from PIL import Image
import io
import os
import json
from datetime import datetime
import uvicorn
from pothole_detector import PotholeDetector

app = FastAPI(title="Pothole Detection API", version="1.0.0")

# Initialize the pothole detector
detector = PotholeDetector()

# Create directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("results", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/detect-pothole")
async def detect_pothole(file: UploadFile = File(...)):
    """
    Upload an image and detect potholes in it
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert PIL image to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Detect potholes
        results = detector.detect(image_cv)
        
        # Save result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_data = {
            "timestamp": timestamp,
            "filename": file.filename,
            "potholes_detected": results["count"],
            "confidence_scores": results["confidences"],
            "bounding_boxes": results["boxes"]
        }
        
        # Save to JSON file
        with open(f"results/{timestamp}.json", "w") as f:
            json.dump(result_data, f, indent=2)
        
        return JSONResponse(content=result_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": detector.is_loaded()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)