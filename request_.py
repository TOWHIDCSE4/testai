import requests
import base64

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def decode_base64_to_image(base64_str, output_path):
    img_data = base64.b64decode(base64_str)
    with open(output_path, 'wb') as output_file:
        output_file.write(img_data)

def send_image_to_server(image_path, server_url):
    # Encode the image to base64
    encoded_image = encode_image_to_base64(image_path)
    
    # Create the payload
    payload = {"image_base64": encoded_image}

    # Send POST request to the server
    response = requests.post(server_url, json=payload)
    
    if response.status_code == 200:
        processed_image_base64 = response.json().get('image')
        print(response.json().get('json'))
        return processed_image_base64
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    # Path to the input image
    input_image_path = "/home/srv/Work/PythonScript/distance_calculation/image/IMG_6895.jpg"  # Replace with your image path
    # Path to save the processed image
    output_image_path = "processed_image.jpg"  # Replace with your output image path
    # FastAPI server URL
    server_url = "http://127.0.0.1:8000/distance_measure/"  # Replace with your FastAPI server URL
    # Send the image to the server and get the processed image
    processed_image_base64 = send_image_to_server(input_image_path, server_url)
    if processed_image_base64:
        # Decode and save the processed image
        decode_base64_to_image(processed_image_base64, output_image_path)
        print(f"Processed image saved as: {output_image_path}")
    else:
        print("Failed to process the image.")
