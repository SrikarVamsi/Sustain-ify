from test import give_image
import io
from PIL import Image
import json
import requests
import streamlit as st
import base64
from PIL import Image





def centre_func():

    st.set_page_config(page_title='DIY Project Generator', page_icon='🛠️', initial_sidebar_state='collapsed')


    st.markdown("""
    <style>
        .centered-title {
            text-align: center;
            padding: 10px;
            border-radius: 5px;
            font-size: 70px;
            font-weight: bold;
        }
    </style>
    <div class="centered-title">DIY Project Generator</div>
""", unsafe_allow_html=True)
    

    st.title('Input')

    if 'upload_img' not in st.session_state:
            st.session_state.upload_img = None

    uploaded_img = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    print(uploaded_img, "🌟 uploaded img")

    st.session_state.upload_img = uploaded_img

    _, coll2, _ = st.columns([1, 1, 1])

    
    if 'op' not in st.session_state:
            st.session_state.op = None


    if 'img' not in st.session_state:
            st.session_state.img = set()


    with coll2 :
        if st.button('Reset'):
            st.session_state.Key = None
            uploaded_img = None
            st.session_state.op = None

            st.session_state.img = set()


    if uploaded_img is None and st.session_state.upload_img is not None:
        image = Image.open(st.session_state.upload_img)
    
        base_width = 300
        w_percent = (base_width / float(image.size[0]))
        h_size = int((float(image.size[1]) * float(w_percent)))
        resized_image = image.resize((base_width, h_size), Image.Resampling.LANCZOS)


        img_buffer = io.BytesIO()
        resized_image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        

        st.markdown(
            f'<div style="text-align: center;">'
            f'<img src="data:image/png;base64,{base64.b64encode(img_buffer.getvalue()).decode()}"/>'
            f'</div>', 
            unsafe_allow_html=True
        )


    elif uploaded_img is not None:
        image = Image.open(uploaded_img)
    
        base_width = 300
        w_percent = (base_width / float(image.size[0]))
        h_size = int((float(image.size[1]) * float(w_percent)))
        resized_image = image.resize((base_width, h_size), Image.Resampling.LANCZOS)


        img_buffer = io.BytesIO()
        resized_image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        

        st.markdown(
            f'<div style="text-align: center;">'
            f'<img src="data:image/png;base64,{base64.b64encode(img_buffer.getvalue()).decode()}"/>'
            f'</div>', 
            unsafe_allow_html=True
        )


        if st.session_state.op is None:
            uploaded_img = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

            json_string = None


            st.write("Generating DIY Project...")



            try: 

                print(bool(st.session_state.op) ," \nCalling gemini API🌟...")

                json_string = requests.post('http://127.0.0.1:8000/', json={'image_data': uploaded_img})

                json_string = json_string.content.decode('utf-8')

                st.session_state.op = json.loads(json.loads(json_string))

            except Exception as e:
                print("mIGHT BE GEMINI ERROR", e)

            st.write("DIY Project Generated!")


            print(st.session_state.op, "🌟 op")


        if 'Key' in st.session_state:
            st.markdown("""
        <style>
            .temp {
                border-radius: 5px;
                font-size: 50px;
                color : black;
            }
        </style>
        <div class="temp">Hav fun:)</div>
    """, unsafe_allow_html=True)
    


        col1, col2, col3 = st.columns([1, 1, 1])

        col1, col2, col3 = st.columns(3)


        
        if 'Key' not in st.session_state:
            st.session_state.Key = None
                
            
        with col1:
                if st.button('Easy', key='Easy'):
                    st.session_state.Key = 'Easy'

        with col2:
                if st.button('Medium', key='Medium'):
                    st.session_state.Key = 'Medium'

        with col3:
                if st.button('Hard', key='Hard'):
                    st.session_state.Key = 'Hard'


        if st.session_state.Key:




            #Title:
            with st.expander("**Project Title**"):
                st.success(f"*{st.session_state.op['Projects'][st.session_state.Key]['DIY_Product']}*")





            # Materials Section
            materials = st.session_state.op['Projects'][st.session_state.Key]['Materials_Required']

            temp = """ """
            if materials:
                for material in materials:
                    temp += f"- *{material['Material']}*: *{material['Quantity']}*\n"
            else:
                temp = "No materials listed."

            with st.expander("**Materials Required**"): st.warning(temp)




            # Steps Section
            temp = """  """
            with st.expander("**Steps**"):
                steps = st.session_state.op['Projects'][st.session_state.Key]['Steps']
                if steps:
                    for step in steps:
                        temp = f"\n **Step {step['Step_Number']}:** *{step['Description']}*\n" + f" \n**Estimated Time** (step {step['Step_Number']}): *{step['Estimated_Time']}*\n" + f" \n**Safety Tips**: *{step['Safety_Tips']}*\n "
                        st.info(temp)
                else:
                    temp = "No steps listed."
                
                


            # Difficulty Level Section
            difficulty = st.session_state.op['Projects'][st.session_state.Key]['Difficulty_Level']
            temp = f" \n**Level**: {difficulty['Level']}\n" + f" \n**Explanation**: {difficulty['Explanation']}\n"
            with st.expander("**Difficulty Level**"): st.error(temp)






            # Image Generation Prompt
            st.markdown("#### Image:")

            st.write('generating the output image...')
            if st.session_state.Key in st.session_state.img:
                st.image(Image.open(f'sample_image_{st.session_state.Key}.png'), caption='Generated Image', use_column_width=True)

            else:
                temp = st.session_state.op['Projects'][st.session_state.Key]['Image_Generation_Prompt']

                give_image(temp)

                with Image.open('sample_image.png') as img:
                    img.save(f'sample_image_{st.session_state.Key}.png')
                    st.session_state.img.add(st.session_state.Key)

            st.write('Generated the image...')


            # Displaying an image
            # st.image(Image.open('sample_image.png'), caption='Generated Image', use_column_width=True)
                   

    else:
        st.markdown(
            """
            <style>
            .custom-text {
                color: red;
                font-size: 20px;
                font-family: monospace;
                font-weight: bold;
            }
            </style>
            <p class="custom-text">Please upload an image.</p>
            """,
            unsafe_allow_html=True
        )


if __name__ == '__main__':
    centre_func()