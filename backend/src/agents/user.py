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

DOC_ADDRESS=os.getenv("DOC_ADDRESS")
DOC_WALLET=os.getenv("DOC_WALLET")

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

class User_Confirmation(Model):
    amount:int
    confirm:bool

@user.on_message(model=PaymentRequest, replies=TransactionInfo)
async def send_payment(ctx: Context, sender: str, msg: PaymentRequest):
    fund_agent_if_low(user.wallet.address())
    transaction = ctx.ledger.send_tokens(msg.wallet_address, msg.amount, msg.denom, user.wallet)
    ctx.storage.set("transaction hash",transaction.tx_hash)
    await ctx.send(DOC_ADDRESS, TransactionInfo(tx_hash=transaction.tx_hash,amount=msg.amount,denom=msg.denom))

@user.on_message(model=TransactionStatus)
async def send_status(ctx: Context, sender: str, msg: TransactionStatus):
    ctx.logger.info(f"Message from {sender}: {msg.status}")
    ctx.storage.set("transaction status",msg.status)

@user.on_query(model=User_Confirmation,replies=PaymentRequest)
async def send_confirmation(ctx: Context, sender: str, msg: User_Confirmation):
    if msg.confirm:
        DENOM = "atestfet"
        await ctx.send(user.address, PaymentRequest(wallet_address=DOC_WALLET,amount=msg.amount,denom=DENOM))

if __name__=="__main__":
    user.run()