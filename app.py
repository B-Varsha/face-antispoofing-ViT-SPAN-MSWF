from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import base64
import torch
import torchvision.transforms as transforms
from PIL import Image
import io
import flask_cors
from ml_model.model import FaceSpoofDetector 
from utils.predictions import pred_and_get_image

app = Flask(__name__)

# Load the pre-trained model
# Load the pre-trained model
model = FaceSpoofDetector()
model_path = 'F:\My projects\FAS\ml_model\justsiw.pth'  # Update the model path if needed
if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    print("Model loaded successfully.")
else:
    print("Error: Model file not found at specified path.")


# Define the transformation for image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_image', methods=['POST'])
def save_image():
    try:
        data = request.json
        img_data = data['image'].split(',')[1]  # Remove data URL prefix
        img_binary = base64.b64decode(img_data)
       
        # Save the image as JPG
        image_name = f"web_capture_img_{len(os.listdir('images')) + 1}.jpg"
        with open(os.path.join('images', image_name), 'wb') as f:
            f.write(img_binary)
       
        return jsonify({'status': 'success', 'message': 'Image saved successfully', 'image_name': image_name})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


from flask import send_file

import os

# @app.route('/predict_image', methods=['POST'])
# def predict_image():
#     try:
#         # Get the base64 encoded image data from the request
#         data = request.json
#         img_data = data['image'].split(',')[1]  # Remove data URL prefix
        
#         # List all files in the 'images' directory
#         image_files = os.listdir('images')
        
#         # Extract the numeric part of each file name and convert to integers
#         image_numbers = [int(file.split('_')[3].split('.')[0]) for file in image_files]
        
#         # Find the maximum image number (i.e., the most recent image)
#         most_recent_image_number = max(image_numbers)
        
#         # Construct the path of the most recently captured image
#         recent_image_name = f"web_capture_img_{most_recent_image_number}.jpg"
#         recent_image_path = os.path.join('images', recent_image_name)
        
#         # Get the predicted image using the model
#         predicted_image = pred_and_get_image(model=model, class_names=['Live', 'Spoofed'], image_path=recent_image_path)
        
#         # Save the predicted image to the "results" folder
#         result_image_path = os.path.join('results', 'result_image.jpg')
#         predicted_image.save(result_image_path)
        
#         # Return the path of the saved result image
#         return jsonify({'status': 'success', 'image_path': result_image_path})
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 400
    
# @app.route('/results/result_image.jpg')
# def serve_results():
#     return send_from_directory('results', 'result_image.jpg')
@app.route('/predict_image', methods=['POST'])
def predict_image():
    try:
        # Get the base64 encoded image data from the request
        data = request.json
        img_data = data['image'].split(',')[1]  # Remove data URL prefix
        
        # List all files in the 'images' directory
        image_files = os.listdir('images')
        
        # Extract the numeric part of each file name and convert to integers
        image_numbers = [int(file.split('_')[3].split('.')[0]) for file in image_files]
        
        # Find the maximum image number (i.e., the most recent image)
        most_recent_image_number = max(image_numbers)
        
        # Construct the path of the most recently captured image
        recent_image_name = f"web_capture_img_{most_recent_image_number}.jpg"
        recent_image_path = os.path.join('images', recent_image_name)
        
        # Get the predicted image using the model
        predicted_image = pred_and_get_image(model=model, class_names=['Live', 'Spoofed'], image_path=recent_image_path)
        
        # List all files in the 'results' directory
        result_files = os.listdir('results')
        
        # Count the number of existing result images
        num_result_images = len(result_files)
        
        # Determine the name for the new result image
        new_image_name = f"result_image_{num_result_images + 1}.jpg"
        
        # Construct the path for the new result image
        result_image_path = os.path.join('results', new_image_name)
        
        # Save the predicted image to the "results" folder
        predicted_image.save(result_image_path)
        
        # Return the path of the saved result image
        return jsonify({'status': 'success', 'image_name': new_image_name})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    
@app.route('/results/<filename>')
def serve_results(filename):
    return send_from_directory('results', filename)

if __name__ == '__main__':
    app.run(debug=True)