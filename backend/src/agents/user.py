from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from uagents.query import query
import os,sys
from dotenv import load_dotenv

from backend.src.protocols.user_proto import makeAppointment, sendAppointment

load_dotenv()

'''
This is the script for user agent
'''

NAME=os.getenv("CUST_NAME")
SEED_PHRASE=os.getenv("CUST_SEED_PHRASE")

user=Agent(
    name=NAME,
    port=8001,
    seed=SEED_PHRASE,
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(user.wallet.address())

user.include(makeAppointment,publish_manifest=True)
user.include(sendAppointment,publish_manifest=True)

class PaymentRequest(Model):
    wallet_address: str
    amount: int
    denom: str
 
class TransactionInfo(Model):
    tx_hash: str
    amount:str
    denom:str

class TransactionStatus(Model):
    status:str

class UserPrompt(Model):
    prompt: str

class Response(Model):
    response: str

if __name__=="__main__":
    user.run()

