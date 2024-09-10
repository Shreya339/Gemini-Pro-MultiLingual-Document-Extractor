import os
from dotenv import load_dotenv

load_dotenv()

import streamlit as st

from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ======= Load Gemini Pro Vision =======

model = genai.GenerativeModel('gemini-1.0-pro-vision-latest')

# ======== Query the LLM ==========

def get_gemini_response(input, image, prompt):
    response=model.generate_content([input, image[0], prompt])
    return response.text

# ======== Input Image Pre-processing to Bytes ====== 

def input_image_preprocess(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

# ========= Streamlit app =============

st.set_page_config(page_title="Multi Lingual Text Extractor & Q&A")

st.header("Multi Lingual Text Extractor and Q&A")
st.subheader("Ask a question about the image")
input=st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Upload Image to extract Text", type=["jpg", "jpeg", "png"])
st.text("Accepted formats: jpeg, jpg, png")


image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
submit=st.button("Ask the question")

# ========= Input Prompt =========

input_prompt = """You are an expert in extracting multilingual text from images.
                I will upload an image. I want you to extraxt the text from the uploaded image
                I want yo to answer any question based on the uploaded image"""
                
# ========= On Submit ======

if submit:
    image_data = input_image_preprocess(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Answer:")
    st.write(response)
    
    
    
# ===== Use Cases =======

""" Document Digitization:

Legal and medical records digitization and querying.
Invoice and Receipt Processing:

Extracting and querying financial data from receipts and invoices.
Customer Support Analysis:

Analyzing customer feedback and product reviews.
Translation Services:

Extracting and translating text for various languages.
Educational Research:

Extracting text from academic documents and notes for analysis.
Compliance Reporting:

Extracting and querying text for regulatory compliance.
Inventory Management:

Managing product details and inventory via extracted text.
Real Estate Management:

Managing property documents and lease agreements.
Marketing Analysis:

Analyzing text from advertisements and brand monitoring.
Insurance Claims Processing:

Extracting and querying information from claims and policy documents. """

