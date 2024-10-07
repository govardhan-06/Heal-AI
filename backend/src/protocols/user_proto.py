from uagents import Context, Model, Protocol
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
import os,re,json,sys,time
from typing import List
from backend.src.utils.exception import customException
import json

#For getting the current date, location of the users
from datetime import datetime
import geocoder
 
makeAppointment=Protocol(name="Appointment",version="1.0")
sendAppointment=Protocol(name='Send_Appointment',version="1.0")

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
 
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

DENOM = "atestfet"  #Since we are in dev phase
DOC_ADDRESS=os.getenv("DOC_ADDRESS")

def agent_location() -> list:
    '''
    This function returns the location of the agent using IP address.
    '''
    try:
        g = geocoder.ip('me')
 
        agent_loc = g.latlng
    except Exception as e:
        raise customException(e,sys)

    return agent_loc

def get_top_doctors(doctors_list, specialization, top_n=5) -> List:
        # Filter doctors by specialization
        filtered_doctors = [doctor for doctor in doctors_list if doctor['specialization'] == specialization]
        
        # Sort doctors by rating in descending order
        sorted_doctors = sorted(filtered_doctors, key=lambda x: x['rating'], reverse=True)
        
        # Return the top N doctors
        return sorted_doctors[:top_n]
 
@makeAppointment.on_query(model=UserPrompt,replies=Response)
async def make_Order(ctx:Context,sender:str,p:UserPrompt):
    '''
    This function handles the messages from the user and decides on the category of doctors to be referred.
    '''
    current_loc=agent_location()
    context=["Gynecologist", "Obstetrician", "Pediatrician", "Neonatologist", "Cardiologist", "Surgeon", "Cardiothoracic Surgeon", "Pulmonologist", "Respiratory Therapist", "Orthopedic Surgeon", "Orthopedic Specialist",]
    
    llm=ChatGroq(temperature=0,model="llama-3.1-70b-versatile",api_key=GROQ_API_KEY)
    chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a virtual medical assistant. Your task is to analyze the disease or symptoms provided by the user and accurately determine the most relevant medical specialization or category of doctor they should consult. Use your knowledge of medical conditions, treatments, and specializations to suggest the best doctor for the user's needs. Respond only with the name of the specialization. Be concise and accurate in your recommendations."
                f"Use this context to choose the specialization: {context}"
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
    )

    chain_suggest = chat_template | llm
    llmOutput = chain_suggest.invoke({"text": p.prompt})

    with open('backend/src/data/indian_doctors_data.json', 'r') as json_file:
        doctors_data = json.load(json_file)

    recommended=get_top_doctors(doctors_data,llmOutput.content)
    recommended=recommended[0]
    
    upcoming_appointments = {
    "appointment_time": recommended['appointment_time'],
    "doctor_details": {
        "doctor_name": recommended['doctor_name'],
        "specialization": recommended['specialization'],
        "rating": recommended['rating'],
        "location": recommended['location'],
        "contact": recommended['contact'],
        "phone": recommended['phone'],
        "latitude": recommended['latitude'],
        "longitude": recommended['longitude'],
    }
    }

    ctx.storage.set("user_location",current_loc)
    ctx.storage.set("user_message",p.prompt)
    ctx.storage.set("upcoming_appointments",upcoming_appointments)
    ctx.storage.set("appointment_time",recommended['appointment_time'])

@sendAppointment.on_query(model=Confirm,replies=Doctor_Message)
async def confirm_order(ctx: Context,sender:str, user_confirmation: Confirm):
    if(user_confirmation.confirm):
        await ctx.send(DOC_ADDRESS, Doctor_Message(location=ctx.storage.get("user_location"), 
                                                   message=ctx.storage.get("user_message"),
                                                   date=ctx.storage.get("appointment_time")))
        

    


    
    

