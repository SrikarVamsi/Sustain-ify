from fastapi import FastAPI, Request
from langchain_core.language_models.chat_models import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import base64
import os
import json


app = FastAPI()

with open('config.json', 'r') as f:
    data = json.load(f)

os.environ['GOOGLE_API_KEY'] = data['GEMINI_API1']


llm = ChatGoogleGenerativeAI(model=data['model'])


@app.post("/")
async def this_is_DIY_really(request : Request):

    req_data = await request.json()

    img_data = req_data['image_data']

    prompt =  """ 
### Instruction

Based on the provided image of an item, please generate the following DIY project information for three different difficulty levels: Easy, Medium, and Hard.

For each difficulty level, include the following details:

1. **DIY Product Description**: Describe the product that can be made using the item in the image. Explain its purpose and potential uses. Incorporate details from the image such as color, texture, and shape to create a vivid description.

2. **Materials Required**: List all materials needed to create the product, specifying the quantity and type. Be specific about the materials shown in the image and any additional items that may be necessary.

3. **Steps**: Provide a detailed step-by-step guide on how to create the product. Ensure each step is clear and actionable, including:
   - **Preparation**: Any preparation needed before starting (e.g., gathering materials, workspace setup).
   - **Instructions**: Detailed instructions for each step, including how to cut, assemble, or apply materials. Reference any specific techniques or tools that relate to the item in the image.
   - **Safety Tips**: Any safety precautions to keep in mind while working on the project, especially those relevant to the materials and methods shown.
   - **Estimated Time**: Provide an estimate of how long each step might take.

4. **Difficulty Level**: Indicate the difficulty level (Easy, Medium, Hard) and explain why it fits that category, considering factors such as required skills, time commitment, and complexity.

5. **Image Generation Prompt**: Provide a detailed text prompt that can be used to generate an image of the finished product for each difficulty level. This description should include visual details such as shape, color, size, materials used, decorative features, and how it relates to the item in the original image.

The output should be structured in JSON format as follows:

"{
    "Projects": {
        "Easy": {
            "DIY_Product": "Description of the easy product.",
            "Materials_Required": [
                {
                    "Material": "Material 1",
                    "Quantity": "1 unit or specific amount"
                },
                {
                    "Material": "Material 2",
                    "Quantity": "2 units or specific amount"
                }
            ],
            "Steps": [
                {
                    "Step_Number": 1,
                    "Description": "Detailed instructions for the first step.",
                    "Estimated_Time": "5 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 2,
                    "Description": "Detailed instructions for the second step.",
                    "Estimated_Time": "10 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 3,
                    "Description": "Detailed instructions for the third step.",
                    "Estimated_Time": "5 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                }
                // Add more steps as needed
            ],
            "Difficulty_Level": {
                "Level": "Easy",
                "Explanation": "Explain why the project is categorized as easy."
            },
            "Image_Generation_Prompt": "Provide a detailed description of the easy product, its colors, shape, and materials used."
        },
        "Medium": {
            "DIY_Product": "Description of the medium product.",
            "Materials_Required": [
                {
                    "Material": "Material 1",
                    "Quantity": "1 unit or specific amount"
                },
                {
                    "Material": "Material 2",
                    "Quantity": "2 units or specific amount"
                }
            ],
            "Steps": [
                {
                    "Step_Number": 1,
                    "Description": "Detailed instructions for the first step.",
                    "Estimated_Time": "10 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 2,
                    "Description": "Detailed instructions for the second step.",
                    "Estimated_Time": "15 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 3,
                    "Description": "Detailed instructions for the third step.",
                    "Estimated_Time": "10 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 4,
                    "Description": "Detailed instructions for the fourth step.",
                    "Estimated_Time": "10 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 5,
                    "Description": "Detailed instructions for the fifth step.",
                    "Estimated_Time": "10 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                }
                // Add more steps as needed
            ],
            "Difficulty_Level": {
                "Level": "Medium",
                "Explanation": "Explain why the project is categorized as medium."
            },
            "Image_Generation_Prompt": "Provide a detailed description of the medium product, its colors, shape, and materials used."
        },
        "Hard": {
            "DIY_Product": "Description of the hard product.",
            "Materials_Required": [
                {
                    "Material": "Material 1",
                    "Quantity": "1 unit or specific amount"
                },
                {
                    "Material": "Material 2",
                    "Quantity": "2 units or specific amount"
                }
            ],
            "Steps": [
                {
                    "Step_Number": 1,
                    "Description": "Detailed instructions for the first step.",
                    "Estimated_Time": "20 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 2,
                    "Description": "Detailed instructions for the second step.",
                    "Estimated_Time": "30 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 3,
                    "Description": "Detailed instructions for the third step.",
                    "Estimated_Time": "15 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 4,
                    "Description": "Detailed instructions for the fourth step.",
                    "Estimated_Time": "25 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 5,
                    "Description": "Detailed instructions for the fifth step.",
                    "Estimated_Time": "20 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 6,
                    "Description": "Detailed instructions for the sixth step.",
                    "Estimated_Time": "15 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                }
                // Add more steps as needed
            ],
            "Difficulty_Level": {
                "Level": "Hard",
                "Explanation": "Explain why the project is categorized as hard."
            },
            "Image_Generation_Prompt": "Provide a detailed description of the hard product, its colors, shape, and materials used."
        }
    }
}"
 """


    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{img_data}"},
            },
        ],
    )

    response = llm([message])

    return response.content

if __name__ == '__main__':

    json_string = this_is_DIY_really('can.jpeg')


    with open('output_prod.json', 'w') as f:
        f.write(json_string)