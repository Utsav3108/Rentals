from fastapi import HTTPException, APIRouter
from twilio.rest import Client
from app.core.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

sms_router = APIRouter()

@sms_router.post("/sms")
async def send_message(to: str, body: str):
    try:
        message = client.messages.create(
            to=to,
            from_=TWILIO_PHONE_NUMBER,
            body=body
        )

        return {"status": "success", "message_sid": message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
