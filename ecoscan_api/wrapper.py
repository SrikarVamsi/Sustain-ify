# DOCS Referred -> https://ai.google.dev/gemini-api/docs/text-generation?lang=python
# API Keys and Playground for Gemini -> https://aistudio.google.com/app/apikey

import os
from dotenv import load_dotenv

import google.generativeai as genai
import PIL.Image

from tavily import TavilyClient, UsageLimitExceededError

from typing import List

import json

import time

# Load variables from the .env file
load_dotenv()


# paths
image_media = "media/images/"
video_media = "media/videos/"


# binding the API to authenticate
genai.configure(api_key=os.environ['GEMINI_API_KEY'])


# model used
model_id = "gemini-1.5-flash"
model = genai.GenerativeModel(model_id)

model_pro_id = "gemini-1.5-pro"
model_pro = genai.GenerativeModel(model_pro_id)

# initializing Tavily Client
tavily_client = TavilyClient(api_key=os.environ['TAVILY_API_KEY'])


# response generated - used only for New Python Version
def responseGemini(response):
    """
    Used to extract text response from a Gemini Response Object.
    """
    return response.parts[0].text


def textInput(model: genai.GenerativeModel, query: str, versionNew: bool = False) -> str | bool:
    """
    Used to give text-input and get text-output from Gemini.
    """
    try:
        response = model.generate_content(query)
        return responseGemini(response) if versionNew else response.text
    except:
        return False


def imageInput(model: genai.GenerativeModel, query: str, image_names: List[str], versionNew: bool = False) -> str | bool:
    """
    Used to give text-input and image-inputs and get text-output from Gemini.
    """
    try:
        images_opened = [PIL.Image.open(image_media + name) for name in image_names]
        response = model.generate_content([query] + images_opened)
        return responseGemini(response) if versionNew else response.text
    except:
        return False


# under testing -> have to explore, can be used only for older python version like 3.10
def streamResponse(model: genai.GenerativeModel, query: str) -> None:
    """
    To Stream and get fast responses Chunk wise constantly in equal intervals
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a story about a magic backpack.", stream=True)
    for chunk in response:
        print(chunk.text)
        print("_" * 80)


# using Tavily search - for real-time contextual reference
def tavilySearch(query: str, tavily_client: TavilyClient = tavily_client) -> str:
    try:
        # Step1 - tavily_client has already been loaded
        # Step 2. Executing a search query
        responses = tavily_client.search(
            query,
            search_depth='advanced',
            max_results=4
            )

        # Step 3. Return the results
        # return [eval(response) for response in responses]
        return [response['content'] for response in responses['results']]
    
    except UsageLimitExceededError:
        return False


# Enum - choosing one option from All
def enumOutput(model: genai.GenerativeModel, query: str, image_names: List[str], enum_values: List[str], versionNew: bool = False):
    try:
        images_opened = [PIL.Image.open(image_media + name) for name in image_names]
        # response = model.generate_content([query + '. Don\'t use markdown format for generating response.'] + images_opened)
        response = model.generate_content(
            [query] + images_opened,
            generation_config=genai.GenerationConfig(
                response_mime_type="text/x.enum",
                response_schema={
                    "type": "STRING",
                    "enum": enum_values # ["Percussion", "String", "Woodwind", "Brass", "Keyboard"],
                },
            ),
        )
        return responseGemini(response) if versionNew else response.text
    except:
        return False

# Giving Output Format to prompt
def getOutPutInFormat(model: genai.GenerativeModel, query: str, image_names: List[str], output_type, versionNew: bool = False):
    try:
        images_opened = [PIL.Image.open(image_media + name) for name in image_names]
        result = model.generate_content(
        [query] + images_opened,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=output_type
        ),
        )
        return responseGemini(result) if versionNew else result.text
    except:
        return False


def typeDocInputNOutputFormat(model: genai.GenerativeModel, query: str, output_type, report_path: str = "media/reports/temp.pdf"):
    # try:
    # sample_pdf = genai.upload_file(report_path)

    video_file = genai.upload_file(path=report_path)

    # load the video file - might take some time to extract features
    while video_file.state.name == "PROCESSING":
        print('.', end='')
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        return False

    # response = model.generate_content(
    #     [query, sample_pdf],
    #     generation_config=genai.GenerationConfig(
    #         response_mime_type="application/json", response_schema=output_type
    #     ),
    #     )
    response = model.generate_content([query, video_file],
                                      generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=output_type
        ),)

    return response.text
    # except:
    #     return False


'''
import enum
from typing_extensions import TypedDict

class Grade(enum.Enum):
    A_PLUS = "a+"
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    F = "f"

class Recipe(TypedDict):
    recipe_name: str
    grade: Grade

model = genai.GenerativeModel("gemini-1.5-pro-latest")

result = model.generate_content(
    "List about 10 cookie recipes, grade them based on popularity",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=list[Recipe]
    ),
)
print(result)  # [{"grade": "a+", "recipe_name": "Chocolate Chip Cookies"}, ...]
'''


# Code for making a Simple ChatBot using Gemini
# ------------------------------------------------------------------------------------------

# model = genai.GenerativeModel("gemini-1.5-flash")
# chat = model.start_chat(
#     history=[
#         {"role": "user", "parts": "Hello"},
#         {"role": "model", "parts": "Great to meet you. What would you like to know?"},
#     ]
# )
# response = chat.send_message("I have 2 dogs in my house.")
# print(response.text)
# response = chat.send_message("How many paws are in my house?")
# print(response.text)
# ------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # testing Text Inputs
    # print(
    #   textInput(
    #       model, 
    #       "I'm Amrit, Im great how are you."
    #           )
    # )
    
    # testing Image Inputs
    # print(
    #     imageInput(
    #         model, 
    #         "What's similar in the images fed.", 
    #         ['test-image-1.jpg', 'test-image-2.jpg']
    #         )
    #     )
    
    # testing Stream Response
    # print(
    #     streamResponse(
    #         model,
    #         "How to make Indian Flavored Rissoto"
    # )
    #     )


    # testing Tavily API
    # realtime_context = tavilySearch("average fertility rate in India")
    # print(realtime_context)
    
    # testing Enum
    # print(enumOutput(model, "I earn 100$ in India a month and I love babies and Im married, would it be feasible to have a baby.", [], ['Yes, It would be nice for you to have one.', 'Wouldn\'t Advice having one :(( Right now.']))
    
    # testing output format
    # print(getOutPutInFormat(model, "Generate 15 excercises to help old aged people. Don't Use Mardown Elements while generating response.", [], list[str]))
    
    
    # print(model.generate_content(['What is the report about', sample_pdf]).text)
    
    # print(typeDocInputNOutputFormat(model, "tell what's in the doc", list[str]))
    ...