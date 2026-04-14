from django.urls import reverse
from django.http import HttpResponseRedirect


from .models import CostumUser
from .views import regex_validator


class PhoneAuthProgressMiddleware:
    def __init__(self, adapted_handler):
        self.get_response = adapted_handler

    def __call__(self, request):
        if request.method == "GET":
            is_auth = request.user.is_authenticated
            path = request.path
            auth_progress = request.session.get("auth_progress")
            password_login_url = reverse("users:login_with_password")
            new_user_password_set_url = reverse("users:password_for_new_user")
            validation_code_url = reverse("users:code_validation")
            referer_url = request.session.get("referer_url")
            redirect_response = HttpResponseRedirect(
                referer_url or reverse("products:index"))
            if is_auth and (path == new_user_password_set_url or path == validation_code_url or path == password_login_url):
                return redirect_response
            response = self.get_response(request)
            if auth_progress == "code_sent" and path == validation_code_url:
                return HttpResponseRedirect(redirect_to=referer_url or reverse("products:index"))
            if auth_progress == "registered_user_password" and path == password_login_url:
                is_reg = request.session.get("is_reg") == True
                phone = request.session.get("phone") if isinstance(
                    request.session.get("phone"), str) else ""
                if is_reg and regex_validator(pattern=r'^(\+98|0)?9\d{9}$', value=phone):
                    pass
                else:
                    return HttpResponseRedirect(redirect_to=referer_url or reverse("products:index"))
            if auth_progress == "new_user_set_password" and path == new_user_password_set_url and request.method != "POST":
                is_reg = request.session.get("is_reg", "not_set")
                phone = request.session.get("phone", "not_set")
                if is_reg == "not_set" or phone == "not_set":
                    return redirect_response
                if is_reg == False and regex_validator(pattern=r'^(\+98|0)?9\d{9}$', value=phone):
                    if not CostumUser.objects.filter(phone=phone).exists():
                        pass
                    else:
                        return redirect_response
            return response
        return self.get_response(request)
