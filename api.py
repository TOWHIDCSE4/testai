from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from source.DistanceMeasure import distanceMeasure

app = FastAPI()
distance_measure_cls = distanceMeasure()

class ImageBase64(BaseModel):
    image_base64: str

def base64_to_cv2_image(base64_str: str):
    # Decode base64 string to bytes
    img_data = base64.b64decode(base64_str)
    # Convert bytes to numpy array
    np_arr = np.frombuffer(img_data, np.uint8)
    # Decode numpy array to OpenCV image
    cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return cv2_img

def cv2_image_to_base64(cv2_img) -> str:
    # Encode OpenCV image to bytes
    _, buffer = cv2.imencode('.jpg', cv2_img)
    # Convert bytes to base64 string
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return img_base64

@app.post("/distance_measure/")
async def distance_measure(image_data: ImageBase64):
    # Convert base64 image to OpenCV format
    cv2_img = base64_to_cv2_image(image_data.image_base64)
    
    distance_measure_cls.get_utils(image=cv2_img)
    json_ = distance_measure_cls.draw_distance()
    

    return json_

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
