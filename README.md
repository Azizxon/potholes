# Pothole Detection System

A free, custom AI-powered pothole detection system that uses computer vision techniques to identify potholes in road images.

## Features

- 🆓 **Free and Open Source**: No paid APIs or proprietary models required
- 📱 **Mobile Compatible**: Works with images from mobile devices
- 🖥️ **Web Interface**: Simple drag-and-drop interface for testing
- 🔍 **Computer Vision**: Uses OpenCV and traditional CV techniques
- 📊 **Detection Results**: Provides confidence scores and bounding boxes
- 💾 **Data Storage**: Saves detection results for analysis

## How It Works

The system uses a combination of computer vision techniques:

1. **Dark Region Detection**: Identifies dark areas that may be potholes
2. **Edge Detection**: Uses Canny edge detection to find irregular shapes
3. **Contour Analysis**: Analyzes shapes and sizes to filter potential potholes
4. **Confidence Scoring**: Generates confidence scores based on darkness and size

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Azizxon/potholes.git
cd potholes
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to `http://localhost:8000`

## API Usage

### Upload Image for Detection

```bash
curl -X POST "http://localhost:8000/detect-pothole" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg"
```

### Response Format

```json
{
  "timestamp": "20231208_143052",
  "filename": "road_image.jpg",
  "potholes_detected": 2,
  "confidence_scores": [0.75, 0.68],
  "bounding_boxes": [[120, 200, 80, 60], [300, 150, 100, 70]]
}
```

## Requirements

- Python 3.7+
- OpenCV
- FastAPI
- TensorFlow (for future ML enhancements)
- PIL/Pillow
- NumPy

## Future Enhancements

- [ ] Train a custom deep learning model for better accuracy
- [ ] Add real-time video processing
- [ ] Implement mobile app integration
- [ ] Add GPS location tagging
- [ ] Severity classification
- [ ] Batch processing capabilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is a proof-of-concept implementation using computer vision techniques. For production use, consider training a custom deep learning model with a larger dataset for improved accuracy.