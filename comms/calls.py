from twilio.rest import TwilioRestClient

from buddy.keys import TWILIO_SID, TWILIO_TOKEN, SERVER_NUMBER, TWILIO_CALLBACK_URL

account_sid = TWILIO_SID
auth_token = TWILIO_TOKEN
server_number = SERVER_NUMBER

client = TwilioRestClient(account_sid, auth_token)

def call_user(phone):
    user_phone = '+1' + phone
    
    call = client.calls.create(
        to=user_phone,
        from_=server_number,
        fallback_method='GET',
        status_callback_method='GET',
        record='false',
        url=TWILIO_CALLBACK_URL
    )
    print(call)
    
def text_user(phone, message):
    user_phone = '+1' + phone
    
    message = client.messages.create(
        body=message,
        to=user_phone,
        from_=server_number
    )
    print(message.sid)