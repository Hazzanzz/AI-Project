import cv2
import os
import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision.models import vgg19, VGG19_Weights

def generate_sketch(image_path, sketch_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: The image at {image_path} could not be loaded.")
        return
    
    # Convert to grayscale for edge detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sketch = cv2.Canny(gray_image, 100, 200)
    cv2.imwrite(sketch_path, sketch)

def preprocess_image(image_path, output_path, vgg):
    transform = transforms.Compose([
        transforms.Resize((1080, 1440)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # Normalization for VGG19
    ])
    
    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0)
    
    # Extract features using VGG19
    with torch.no_grad():
        features = vgg.features(image_tensor)
    
    # Average the feature maps to reduce the channels to 3
    feature_maps = features.squeeze(0).mean(dim=0)
    
    # Normalize the feature maps to be in range [0, 1]
    feature_maps = (feature_maps - feature_maps.min()) / (feature_maps.max() - feature_maps.min())
    
    # Convert the tensor back to an image
    enhanced_image = transforms.ToPILImage()(feature_maps)
    
    enhanced_image.save(output_path)

# Define your folders
input_folder = r"C:\Users\hassz\OneDrive\Documents\AI_project\Import Images"
sketch_folder = r"C:\Users\hassz\OneDrive\Documents\AI_project\Export Images\sketch"
processed_folder = r"C:\Users\hassz\OneDrive\Documents\AI_project\Export Images\processed"

# Load VGG19 model
weights = VGG19_Weights.IMAGENET1K_V1
vgg = vgg19(weights=weights).eval()

# Check if input folder exists
if not os.path.exists(input_folder):
    print(f"Error: The input folder {input_folder} does not exist.")
else:
    # Ensure the output directories exist
    os.makedirs(sketch_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)

    # Sketch generation
    for image_name in os.listdir(input_folder):
        image_path = os.path.join(input_folder, image_name)
        sketch_path = os.path.join(sketch_folder, image_name)
        generate_sketch(image_path, sketch_path)

    # Image preprocessing
    for image_name in os.listdir(sketch_folder):
        image_path = os.path.join(sketch_folder, image_name)
        output_path = os.path.join(processed_folder, image_name)
        preprocess_image(image_path, output_path, vgg)
