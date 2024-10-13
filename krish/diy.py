import requests
import base64


name = 'ruffless'
dtype = 'jpeg'


with open(f'inputs/{name}.{dtype}', 'rb') as img_file:
    img_data = base64.b64encode(img_file.read()).decode('utf-8')

print("1.) Img encoded...")



cont = requests.post('http://127.0.0.1:8000/', json={'image_data': img_data})
json_string = cont.content.decode('utf-8')

print("2.) Got contnet...")




with open(f'output_json/output_prod_{name}.json', 'w') as f:
    f.write(json_string)

print('3.) Json File created...')