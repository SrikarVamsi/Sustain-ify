from openai_image_gen import generateImages
import uuid
import time

def generate_unique_id():
    """Generates a unique random ID using a combination of UUID and timestamp."""
    unique_id = str(uuid.uuid4())  # Generate a UUID
    timestamp = int(time.time() * 1000)  # Get current timestamp in milliseconds
    return f"{unique_id}-{timestamp}"

# DIY - PipeLine ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def give_image(prompt) -> dict:

    id_generated = generate_unique_id()

    image_in_b64 = generateImages(
        prompt,
        id_generated
        )
    
    return image_in_b64


import base64

def decodeImage(output_path: str, b64_data):

    # Decode base64 to binary data
    image_data = base64.b64decode(b64_data)

    # Define the output file path (e.g., PNG format)
    output_file = output_path

    # Write the image data to a file
    with open(output_file, 'wb') as image_file:
        image_file.write(image_data)
    
    print("done")


if __name__ == "__main__":
    decodeImage("sample_image.png", give_image("A pig eating Grass."))