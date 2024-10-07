from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from uagents.query import query
import os,sys
from dotenv import load_dotenv

from backend.src.protocols.postCare_proto import postCare

load_dotenv()

'''
This is the script for care agent
'''

NAME=os.getenv("HEAL_NAME")
SEED_PHRASE=os.getenv("HEAL_SEED_PHRASE")

care=Agent(
    name=NAME,
    port=8003,
    seed=SEED_PHRASE,
    endpoint=["http://127.0.0.1:8003/submit"],
)

fund_agent_if_low(care.wallet.address())

care.include(postCare,publish_manifest=True)

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
    care.run()
