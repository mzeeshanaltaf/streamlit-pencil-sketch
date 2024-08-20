import streamlit as st
import numpy as np
from PIL import Image
from io import BytesIO
import cv2
from datetime import datetime


def pencil_sketch(input_image):
    img_gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    img_invert = cv2.bitwise_not(img_gray)
    img_smoothing = cv2.GaussianBlur(img_invert, (21, 21), sigmaX=0, sigmaY=0)
    final_image = cv2.divide(img_gray, 255 - img_smoothing, scale=255)
    return final_image


def download_sketch(sketch):
    image = Image.fromarray(sketch)

    # Save the image to a BytesIO object
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


page_title = "Pencil Sketch"
page_icon = "✏️"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")

st.title(page_title)
st.write(":green[***✏️ Turn Your Photos into Stunning Pencil Sketches! 🎨***]")
st.write("Upload your favorite photos and watch them transform into realistic pencil sketches with just a click! "
         "Perfect for adding an artistic touch to your memories. 📸✨")
st.subheader("Upload an Image")
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_image:
    # Open the uploaded image, convert it to format readable by opencv, resize and change to gray scale
    image_o = np.array(Image.open(uploaded_image))

    st.subheader("Result")
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1:
        st.write(':blue[***Input Picture***]')
        st.image(image_o)

    with col2:
        st.write(':blue[***Pencil Sketch***]')
        p_sketch = pencil_sketch(image_o)
        st.image(p_sketch)

    st.subheader('Download Sketch')

    # Convert the image to BytesIO object so that it could be downloaded
    buffer = download_sketch(p_sketch)

    # Create a file name with current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"image_{current_time}.png"

    st.download_button("Download", data=buffer, file_name=file_name, mime="image/png", type="primary")
