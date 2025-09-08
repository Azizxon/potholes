# API Documentation

## Pothole Detection API

This API provides endpoints for detecting potholes in images using computer vision techniques.

### Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the API and model are working properly.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 2. Detect Potholes
**POST** `/detect-pothole`

Upload an image to detect potholes.

**Parameters:**
- `file` (multipart/form-data): Image file (JPEG, PNG, etc.)

**Example Request:**
```bash
curl -X POST "http://localhost:8000/detect-pothole" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@road_image.jpg"
```

**Response:**
```json
{
  "timestamp": "20231208_143052",
  "filename": "road_image.jpg",
  "potholes_detected": 2,
  "confidence_scores": [0.75, 0.68],
  "bounding_boxes": [[150, 200, 80, 60], [300, 150, 100, 70]]
}
```

**Response Fields:**
- `timestamp`: When the analysis was performed
- `filename`: Original filename of uploaded image
- `potholes_detected`: Number of potholes found
- `confidence_scores`: Array of confidence scores (0.0 to 1.0)
- `bounding_boxes`: Array of [x, y, width, height] coordinates

### 3. Web Interface
**GET** `/`

Access the interactive web interface for easy testing.

## Error Responses

### 400 Bad Request
```json
{
  "detail": "File must be an image"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error processing image: <error_message>"
}
```

## Integration Examples

### Python
```python
import requests

# Upload and detect
with open('road_image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/detect-pothole', files=files)
    result = response.json()
    print(f"Found {result['potholes_detected']} potholes")
```

### JavaScript
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('/detect-pothole', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    console.log(`Found ${data.potholes_detected} potholes`);
});
```

### Mobile App Integration
The API can be easily integrated into mobile applications:

```swift
// iOS Swift example
let url = URL(string: "http://your-server.com/detect-pothole")!
var request = URLRequest(url: url)
request.httpMethod = "POST"

let formData = MultipartFormData()
formData.append(imageData, withName: "file", fileName: "image.jpg", mimeType: "image/jpeg")

request.setValue("multipart/form-data; boundary=\(formData.boundary)", forHTTPHeaderField: "Content-Type")
request.httpBody = formData.encode()
```

## Data Storage

Results are automatically saved to the `results/` directory as JSON files with timestamps for later analysis and reporting.

## Deployment

### Docker
```bash
docker build -t pothole-detector .
docker run -p 8000:8000 pothole-detector
```

### Production Considerations
- Use HTTPS in production
- Implement rate limiting
- Add authentication if needed
- Configure proper logging
- Set up monitoring and alerting