from flask import Flask, request, jsonify
from PIL import Image
import torch
from torchvision import transforms
import io

# Load pre-trained StyleGAN model (for example purposes, replace with actual model)
model = torch.hub.load('facebookresearch/pytorch_GAN_zoo:hub', 'PGAN', model_name='celebAHQ-512', pretrained=True)

app = Flask(__name__)

def transform_image(image_bytes):
    preprocess = transforms.Compose([
        transforms.Resize(512),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(image_bytes))
    return preprocess(image).unsqueeze(0)

@app.route('/api/generate-portrait', methods=['POST'])
def generate_portrait():
    file = request.files['sketch']
    img_bytes = file.read()
    sketch_tensor = transform_image(img_bytes)

    # Generate the portrait (replace with actual model inference)
    with torch.no_grad():
        portrait_tensor = model(sketch_tensor)

    # Convert tensor to image
    portrait_image = transforms.ToPILImage()(portrait_tensor.squeeze())

    # Save the image to a file
    portrait_path = f"uploads/generated-{file.filename}"
    portrait_image.save(portrait_path)

    return jsonify({'portraitUrl': f"http://localhost:3000/{portrait_path}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
