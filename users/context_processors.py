from .models import CostumUser


def cities_list(request):
    return {"cities" : CostumUser.CITY_CHOICES}


def error_in_sms_send(request):
    error_sending_sms = request.session.get("error_send_sms")
    if error_sending_sms:
        del request.session["error_send_sms"]

    return {"error_send_sms_alert" : error_sending_sms}