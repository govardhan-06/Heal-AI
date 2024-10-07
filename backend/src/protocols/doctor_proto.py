from uagents import Context, Model, Protocol
import os,sys,uuid,geocoder
from geopy.distance import geodesic

from backend.src.utils.exception import customException

CUST_ADDRESS=os.getenv("CUST_ADDRESS")

class Doctor_Message(Model):
    location:list
    message:str
    date:str

class Confirm(Model):
    confirm:bool

class Confirm_Appointment(Model):
    message:str

take_Appointments=Protocol("Taking Appointments",version="1.0")
accept_Appointments=Protocol("Accept Appointments",version="1.0")

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

@take_Appointments.on_message(model=Doctor_Message)
async def recieve_Orders(ctx:Context,sender:str,newAppointment:Doctor_Message):
    '''
    Function to receive orders from the customer agent
    '''
    doc_loc=agent_location()
    ctx.logger.info(f"New Appointment received from address {sender}")

    upcoming_sessions={
        "date":newAppointment.date,
        "message":newAppointment.message,
        "location":newAppointment.location,
    }

    ctx.storage.set("upcoming_sessions",upcoming_sessions)

@accept_Appointments.on_query(model=Confirm,replies=Confirm_Appointment)
async def accept_Orders(ctx:Context,sender:str,req:Confirm):

    if req.confirm:
        doc_message=f"Appointment confirmed. Please reach the clinic before 10 mins of the scheduled time"
        await ctx.send(CUST_ADDRESS,Confirm_Appointment(message=doc_message))

    else:
        doc_message=f"Sorry for the inconvenience!! Currently not accepting any appointments"
        await ctx.send(CUST_ADDRESS,Confirm_Appointment(message=doc_message))


    




