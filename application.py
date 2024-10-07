from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import sys,uvicorn,os,json
from starlette.responses import JSONResponse
import subprocess
from dotenv import load_dotenv
from uagents.query import query
from uagents import Model
from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
from backend.src.utils.exception import customException
from backend.src.utils.logger import logging

load_dotenv()

CUST_ADDRESS=os.getenv("CUST_ADDRESS")
DOC_ADDRESS=os.getenv("DOC_ADDRESS")
HEAL_ADDRESS=os.getenv("HEAL_ADDRESS")

CUST_STORAGE=os.getenv("CUST_STORAGE")
DOC_STORAGE=os.getenv("DOC_STORAGE")
HEAL_STORAGE=os.getenv("HEAL_STORAGE")

class UserPrompt(Model):
    prompt: str

class Confirm(Model):
    confirm:bool

class File_path(Model):
    file_path:str

class User_Confirmation(Model):
    amount:int
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

@app.post("/healer")
async def run_healer():
    '''
    This function is used to run the healer agent.
    '''
    try:
        subprocess.Popen(["python", "backend/src/agents/postCare.py"])
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
    This function is used to confirm the appointment with the doctor agent.
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
    This function is used to get the upcoming sessions from the user agent.
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

@app.post("/confirmVisit")
async def confirmVisit(req: bool):
    '''
    For User
    This function is used to confirm the visit with the doctor.
    '''
    try:
        if(req):
            with open(CUST_STORAGE, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    raise customException(f"Error reading JSON file: {str(e)}", sys)
                
            amountpaid=25
            await query(destination=CUST_ADDRESS, message=User_Confirmation(amount=amountpaid,confirm=req), timeout=20.0)
            return JSONResponse(content={"message": "Doctor Visit confirmed, Get well soon!!"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Appointment cancelled!! Sorry for the inconvenience..."}, status_code=200)
    except customException as e:
        logging.error(e)
        return JSONResponse(content={"error": {e}}, status_code=500)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    '''
    For Healer
    This function is used to upload documents and suggest dosage, health tips.
    '''
    # Save the uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    
    with open(temp_file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    try:
        await query(destination=HEAL_ADDRESS, message=File_path(file_path=temp_file_path), timeout=10.0)
        # Open and read the JSON file
        with open(HEAL_STORAGE, 'r') as f:
            logging.info("Fetching data from agent storage")
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise customException(f"Error reading JSON file: {str(e)}", sys)
        
        return JSONResponse(content={"message": "Success","appointment":data["recommendations"]}, status_code=200)

    except customException as e:
        logging.error(e)
        return JSONResponse(content={"error": {e}}, status_code=500)
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
