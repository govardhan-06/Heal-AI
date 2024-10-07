from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import sys,uvicorn,os,json
from starlette.responses import JSONResponse
import subprocess
from dotenv import load_dotenv
from uagents.query import query
from uagents import Model
from backend.src.utils.exception import customException
from backend.src.utils.logger import logging

load_dotenv()

CUST_ADDRESS=os.getenv("CUST_ADDRESS")
DOC_ADDRESS=os.getenv("DOC_ADDRESS")

CUST_STORAGE=os.getenv("CUST_STORAGE")
DOC_STORAGE=os.getenv("DOC_STORAGE")

class UserPrompt(Model):
    prompt: str

class Confirm(Model):
    confirm:bool

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    '''
    This function is used to redirect to the swaggerUI page.
    '''
    return RedirectResponse(url="/docs")
 
@app.post("/user")
async def run_user():
    '''
    This function is used to run the user agent.
    '''
    try:
        subprocess.Popen(["python", "backend/src/agents/user.py"])
    except Exception as e:
        raise customException(e,sys)

@app.post("/doctor")
async def run_doctor():
    '''
    This function is used to run the doctor agent.
    '''
    try:
        subprocess.Popen(["python", "backend/src/agents/doctor.py"])
    except Exception as e:
        raise customException(e,sys)

@app.post("/prompt")
async def cust_prompt(prompt:str):
    '''
    For User
    This function is used to send a prompt to the user agent.
    Returns the model response as a JSON
    '''
    try:
        await query(destination=CUST_ADDRESS, message=UserPrompt(prompt=prompt), timeout=10.0)
        # Open and read the JSON file
        with open(CUST_STORAGE, 'r') as f:
            logging.info("Fetching data from agent storage")
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise customException(f"Error reading JSON file: {str(e)}", sys)
        
        upcoming_appointments=data['upcoming_appointments']
        return JSONResponse(content={"message": "Success","appointment":upcoming_appointments}, status_code=200)

    except customException as e:
        logging.error(e)
        return JSONResponse(content={"error": {e}}, status_code=500)

@app.post("/confirm")
async def cust_confirmation(req:bool):
    '''
    For User
    This function is used to confirm the appointment with the customer agent.
    '''
    try:
        if req:
            await query(destination=CUST_ADDRESS, message=Confirm(confirm=req), timeout=10.0)
            return JSONResponse(content={"message": "Appointment Confirmed"}, status_code=200)
        
        else:
            return JSONResponse(content={"message": "Sorry!! lets do it once again..."}, status_code=200)

    except customException as e:
        logging.error(e)
        return JSONResponse(content={"error": {e}}, status_code=500)

@app.get("/upcoming_sessions")
async def get_current_orders():
    '''
    For Doctor
    This function is used to get the ucpmoing sessions from the user agent.
    Returns the upcoming sessions as a JSON
    '''
    try:
        # Open and read the JSON file
        with open(DOC_STORAGE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise customException(f"Error reading JSON file: {str(e)}", sys)

        return JSONResponse(content={"message": "Success","upcoming_sessions":data['upcoming_sessions']}, status_code=200)

    except customException as e:
        logging.error(e)
        return JSONResponse(content={"error": {e}}, status_code=500)

@app.post("/accept_appointment")
async def accept_order(req:bool):
    '''
    For Doctor
    This function is used to accept the appointments.
    '''
    if(req):
        try:
            await query(destination=DOC_ADDRESS, message=Confirm(confirm=req), timeout=15.0)
            return JSONResponse(content={"message": "Appointments Accepted"}, status_code=200)

        except customException as e:
            logging.error(e)
            return JSONResponse(content={"error": {e}}, status_code=500)
    else:
        return JSONResponse(content={"message": "Currently we are not accepting any appointments"}, status_code=200)

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
