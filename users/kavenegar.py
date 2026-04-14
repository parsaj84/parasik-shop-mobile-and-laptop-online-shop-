from kavenegar import *


def send_sms( receptor, message):
    success = True
    error =False
    try:
        api = KavenegarAPI(
            '7851776B3959586169615051382F65414E624E4D556F4F49585337475A6D64684232386D6B456F736577343D')
        params = {
            'sender': '0018018949161',  # optional
            'receptor': receptor,  # multiple mobile number, split by comma
            'message': message,
        }
        response = api.sms_send(params)
    except APIException as e:
        error = True
        success = False
    except HTTPException as e:
        error = True
        success = False
    return {"error" : error, "success" : success}