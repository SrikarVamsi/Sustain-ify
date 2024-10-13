
import openai

import datetime

import base64
import io
import PIL.Image

import os
from dotenv import load_dotenv



# Load environment variables from the .env file
load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# convert images ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def convert_b64_to_image(b64_string, image_path):
    """Converts a base64-encoded string to a PIL Image object.

    Args:
        b64_string (str): The base64-encoded string.

    Returns:
        PIL.Image: The decoded PIL Image object.
    """

    try:
        # Decode the base64 string
        image_data = base64.b64decode(b64_string)

        # Create an image from the decoded data
        image = PIL.Image.open(io.BytesIO(image_data))

        image.save(image_path)
    except Exception as e:
        print(f"Error converting base64 to image: {e}")
        return None


# generate images ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def generateImages(prompt, id_generated, number_of_images=1):
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    response_format="b64_json",
    n=number_of_images,
    )

    first_image = response.data[0].b64_json
    # second_image = response.data[1].b64_json

    directory_path = "sample_image.png"

    convert_b64_to_image(first_image, directory_path)
    # convert_b64_to_image(second_image, directory_path + f"{str(datetime.datetime.now())}.jpg")

    return first_image #[first_image, second_image]


if __name__ == "__main__":
    # getImages(uploadImageAndGetResponse("static/images/coke.png", generate_prompt_to_create_final_diy_image.replace("{0}", "Pen Holder")), 1)
    pass