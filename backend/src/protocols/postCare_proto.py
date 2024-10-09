from uagents import Context, Model, Protocol
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
import os,re,json,sys,time
from typing import List
from backend.src.utils.exception import customException
import json
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()
 
postCare=Protocol(name='Post Care',version="1.0")

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
 
class UserPrompt(Model):
    prompt:str

class Response(Model):
    response:str

class Confirm(Model):
    confirm:bool

class Doctor_Message(Model):
    location:list
    message:str
    date:str

class File_path(Model):
    file_path:str

DOC_ADDRESS=os.getenv("DOC_ADDRESS")

def ocr_image(image_path):
    """Perform OCR on a single image."""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def ocr_pdf(pdf_path):
    """Perform OCR on a PDF file."""
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path)
        full_text = ""

        for i, image in enumerate(images):
            # Optionally save images to disk for debugging
            # image.save(f"page_{i+1}.png", 'PNG')
            text = pytesseract.image_to_string(image)
            full_text += f"Page {i+1}:\n{text}\n"

        return full_text
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

@postCare.on_query(model=File_path,replies=Response)
async def post_care(ctx:Context,sender:str,path:File_path):
    input_file = path.file_path
    load_dotenv()
    GROQ_API_KEY=os.getenv("GROQ_API_KEY")

    if input_file.lower().endswith('.pdf'):
        text = ocr_pdf(input_file)
    elif input_file.lower().endswith(('.png', '.jpg', '.jpeg')):
        text = ocr_image(input_file)
    else:
        print("Unsupported file type. Please provide a PDF or an image file.")
        return

    if text:
        llm=ChatGroq(temperature=0,model="llama-3.1-70b-versatile",api_key=GROQ_API_KEY)
        chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are a virtual medical assistant. Your task is to analyze the provided text from medical documents, such as prescriptions or lab reports, and offer accurate recommendations based on the information contained within them."
                    "If the document is a prescription, ensure that you mention the dosage of each medicine prescribed and specify the purpose of each medication."
                    "If the document is a lab report, check the reported values for correctness, indicate which values are within normal ranges and which are not, and suggest health tips to optimize these values for better health."
                    "Utilize your knowledge of medical conditions, treatments, and relevant medical guidelines to suggest necessary actions, potential diagnoses, or additional tests the user may need to consider. Respond only with clear and actionable suggestions. Be concise and precise in your recommendations."
                )
            ),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
        )

        chain_suggest = chat_template | llm
        llmOutput = chain_suggest.invoke({"text": text})

        suggestions=llmOutput.content

        ctx.storage.set("patient",sender)
        ctx.storage.set("recommendations",suggestions)

        
