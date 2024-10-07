from uagents import Agent,Context,Model
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low

import os,sys
from dotenv import load_dotenv
from backend.src.protocols.doctor_proto import take_Appointments,accept_Appointments

load_dotenv()

NAME=os.getenv("DOC_NAME")
SEED_PHRASE=os.getenv("DOC_SEED_PHRASE")

CUST_ADDRESS=os.getenv("CUST_ADDRESS")

doctor=Agent(
    name=NAME,
    port=8002,
    seed=SEED_PHRASE,
    endpoint=["http://127.0.0.1:8002/submit"],
)

fund_agent_if_low(doctor.wallet.address())

doctor.include(take_Appointments,publish_manifest=True)
doctor.include(accept_Appointments,publish_manifest=True)

class TransactionInfo(Model):
    tx_hash: str
    amount:str
    denom:str

class TransactionStatus(Model):
    status:str

@doctor.on_message(model=TransactionInfo,replies=TransactionStatus)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
    ctx.logger.info(f"Received transaction info from {sender}: {msg}")
 
    tx_resp = await wait_for_tx_to_complete(msg.tx_hash, ctx.ledger)
    coin_received = tx_resp.events["coin_received"]
 
    if (
        coin_received["receiver"] == str(doctor.wallet.address())
        and coin_received["amount"] == f"{msg.amount}{msg.denom}"
    ):
        ctx.logger.info(f"Transaction was successful: {coin_received}")
 
        ctx.storage.set('paymentStatus',f"Received payment from {sender}. Thank You")
        ctx.storage.set('transaction hash',msg.tx_hash)
        await ctx.send(CUST_ADDRESS,TransactionStatus(status=f"Received payment from {sender}. Thank You"))

if __name__=="__main__":
    print(str(doctor.wallet.address()))
    doctor.run()

