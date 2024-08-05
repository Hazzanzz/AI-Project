import os

image_path = 'path/to/your/image.jpg'
absolute_image_path = os.path.abspath(image_path)
print(absolute_image_path)  # Print the absolute path to verify it

# Check if the absolute path exists
print(os.path.exists(absolute_image_path))  # This should print True if the path is correct