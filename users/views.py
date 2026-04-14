from django.http import HttpResponse
from kavenegar import *
from django.shortcuts import render
from django.core.mail import send_mail

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.template.loader import render_to_string
from django import forms
from django.views.decorators.http import require_POST


from .forms import UserUpdateAccount
from .models import CostumUser, EmailExist, PhoneExist, Address
from products.models import Product
from orders.models import Order
from .kavenegar import send_sms

from datetime import date
import time
import random
import re


    

def city_province_html_renderer(request):
    province_option = CostumUser.PROVINCE_CHOICES
    cities = []
    province = request.user.province if request.user.province else "thr"
    for city in CostumUser.CITY_CHOICES:
        if city[0][0:3] == province:
            cities.append(city)
    city_options = render_to_string(
        "partials/city_set_ajax.html", {"cities": cities})
    province_options = render_to_string(
        "partials/province_options.html", {"provinces": province_option, "province": province})
    return [city_options, province_options]


def regex_validator(pattern, value):
    return re.fullmatch(pattern=pattern, string=value)


def user_register(request):
    is_reg = True
    next_url = request.GET.get("next")
    if request.session.get("auth_progress"):
        del request.session["auth_progress"]
    if next_url:
        request.session["next_url"] = next_url
    if request.session.get("error_send_sms"):
        del request.session["error_send_sms"]
    if request.session.get("generate_for"):
        del request.session["generate_for"]
    if request.session.get("code"):
        del request.session["code"]
    if request.session.get("code_gen_time"):
        del request.session["code_gen_time"]
    if request.session.get("phone"):
        del request.session["phone"]
    if request.session.get("is_reg"):
        del request.session["is_reg"]
    error_invalid_reg_token = None
    error_send_validation_code = None
    error_sending_sms = False
    if request.session.get("error_send_sms", "empty") != "empty":
        del request.session["error_send_sms"]
    if request.method == "POST":
        reg_token = request.POST.get("reg_token")
        if regex_validator(pattern=r'^(\+98|0)?9\d{9}$', value=reg_token):
            is_reg = CostumUser.objects.filter(phone = reg_token).exists()
            code = str(random.randint(10000, 99999))
            send_sms_result = send_sms(receptor=reg_token, message=f"کد ورود شما به پاراسیک شاپ {code}")
            if send_sms_result.get("success"):
                code_gen_time = time.time()
                request.session["generate_for"] = reg_token
                request.session["code"] = code
                request.session["code_gen_time"] = code_gen_time
                request.session["phone"] = reg_token
                request.session["is_reg"] = is_reg
                return HttpResponseRedirect(reverse("users:code_validation"))
            else:
                error_sending_sms = True
                request.session["error_send_sms"] = error_sending_sms
                if is_reg:
                    request.session["phone"] = reg_token
                    request.session["is_reg"] = is_reg
                    return HttpResponseRedirect(reverse("users:login_with_password"))  
        else:
            error_invalid_reg_token = True
    else:
        if referer_url := request.META.get("HTTP_REFERER"):
            request.session["referer_url"] = referer_url
            

        if request.session.get("email"):
            del request.session["email"]
            
        if request.session.get("phone"):
            del request.session["phone"]
            
    return render(request, "register/login.html", {"error_send_validation_code": error_send_validation_code,"error_sending_sms" : error_sending_sms ,"is_reg" : is_reg,"error_invalid_reg_token": error_invalid_reg_token})


def code_validation(request):
    code = request.session.get("code")
    is_reg = request.session.get("is_reg")
    request.session["auth_progress"] = "code_sent"
    if not code:
        redirect_to = reverse("users:login_with_password") if is_reg else reverse("products:index") 
        return HttpResponseRedirect(redirect_to)
    error = None
    error_active = None
    error_404 = None
    phone = request.session.get("phone")
    code_gen_time = request.session.get("code_gen_time")
    remaining_time_text = None
    referer_url = request.session.get("referer_url")
    remaining_time = int(180 - (time.time() - code_gen_time)
                         ) if code_gen_time else None

    if remaining_time and remaining_time > 0:
        minutes = int(remaining_time / 60)
        secounds = int(remaining_time % 60)
        if minutes < 1:
            minutes = f"0{minutes}"
        if secounds < 10:
            secounds = f"0{secounds}"
        remaining_time_text = f"{minutes}:{secounds}"
    if request.method == "POST":
        code_units = [request.POST.get("code_unit_1"), request.POST.get("code_unit_2"), request.POST.get(
            "code_unit_3"), request.POST.get("code_unit_4"), request.POST.get("code_unit_5")]
        client_code = "".join(code_units)
        if client_code == code:
            del request.session["code"]
            if time.time() - code_gen_time <= 180:
                del request.session["code_gen_time"]
                if is_reg:
                    user = CostumUser.objects.get(phone=phone)
                    if user.is_active:
                        cart = request.session["cart"] if request.session.get(
                            "cart") else None
                        login(request, user)
                        request.session["cart"] = cart
                        if request.session.get("phone"):
                            del request.session["phone"]
                        if next_url := request.session.get("next_url"):
                            del request.session["next_url"]
                            return HttpResponseRedirect(next_url)
                        if referer_url:
                            del request.session["referer_url"]
                            return HttpResponseRedirect(referer_url)
                        return HttpResponseRedirect(reverse("products:index"))
                    else:
                        error_active = "کاربر غیر فعال است."
                else:
                    return HttpResponseRedirect(reverse("users:password_for_new_user"))
            else:
                error = True
        else:
            error = True

    return render(request, "register/code_validation.html", context={"error": error, "error_404": error_404, "error_active": error_active, "phone": phone, "remaining_time": remaining_time, "remaining_time_text": remaining_time_text, "is_reg": is_reg})


@login_required
def logout_user(request):
    cart = request.session["cart"]
    logout(request)
    request.session["cart"] = cart
    return HttpResponseRedirect(reverse("users:register"))


def new_user_create(request):
    phone = request.session.get("phone")
    request.session["auth_progress"] = "new_user_set_password"
    error_send_sms = request.session.get("error_send_sms")
    error = False
    referer_url = request.session.get("referer_url")
    error_invalid_password_confirm = False
    if request.method == "POST":
        password = request.POST.get("password")
        password_confirm = request.POST.get("password-confirm")
        if password == password_confirm:
            if phone:
                try:
                    user = CostumUser.user_manager.create_user(phone=phone, password=password)
                    cart = request.session.get("cart")
                    login(request, CostumUser.objects.get(phone=phone))
                    request.session["cart"] = cart
                    if next_url := request.session.get("next_url"):
                        del request.session["next_url"]
                        return HttpResponseRedirect(next_url)
                    if referer_url:
                        del request.session["referer_url"]
                        return HttpResponseRedirect(referer_url)
                    return HttpResponseRedirect(reverse("products:index"))
                except PhoneExist:
                    error = "خطا!"
        else:
            error_invalid_password_confirm = "تایید رمز عبور باید رمز عبور یکسان باشد."
    return render(request, "register/password_submit_optimized.html", {"error": error, "error_invalid_password_confirm": error_invalid_password_confirm, "error_send_sms" :error_send_sms })


def login_with_password(request):
    phone = request.session.get("phone")
    referer_url = request.session.get("referer_url")
    is_reg = request.session.get("is_reg")
    request.session["auth_progress"] = "registered_user_password"
    error = None
    if request.method == "POST":
        password = request.POST.get("password")
        if is_reg:
            if phone:
                try:
                    user = CostumUser.objects.get(phone=phone)
                    if user.is_active:
                        if user.check_password(password):
                            cart = request.session.get("cart")
                            login(request, user)
                            request.session["cart"] = cart
                            if request.session.get("phone"):
                                del request.session["phone"]
                            if next_url := request.session.get("next_url"):
                                del request.session["next_url"]
                                return HttpResponseRedirect(next_url)
                            if referer_url:
                                del request.session["referer_url"]
                                return HttpResponseRedirect(referer_url)
                            return HttpResponseRedirect(reverse("products:index"))
                        else:
                            error = "رمز عبور اشتباه است!"
                    else:
                        error = "کاربر غیر فعال است!"
                except CostumUser.DoesNotExist:
                    error = "خطا!"

            if not phone:
                error = "خطا"
        else:
            error = "خطا!"
    return render(request, "register/login_with_password.html", {"is_reg": is_reg, "error": error, "is_reg" : is_reg, "error_sending_sms" : request.session.get("error_send_sms")})


def add_to_facourite(request):
    is_authenticated = None
    error_404 = False
    in_favourite = None
    product_id = request.POST.get("product_id")
    if request.user.is_authenticated:
        is_authenticated = True
        try:
            product = Product.objects.prefetch_related(
                "favourite_by").get(pk=product_id)
            if request.user in product.favourite_by.all():
                product.favourite_by.remove(request.user)
                in_favourite = False
            else:
                product.favourite_by.add(request.user)
                in_favourite = True

        except Product.DoesNotExist:
            error_404 = False
    else:
        is_authenticated = False

    context = {
        "in_favourite": in_favourite,
        "is_authenticated": is_authenticated,
        "error": error_404
    }
    return JsonResponse(context)


@login_required
def dashboard(request):
    orders = Order.objects.order_by(
        "-date_created").filter(buyer=request.user)
    orders_count = orders.count()
    recent_orders = Order.objects.order_by(
        "-date_created").filter(buyer=request.user)[0:3]
    return render(request, "users/dashboard.html", {"orders": recent_orders, "orders_count": orders_count})


@login_required
def add_address(request):
    error = None
    [city_options , province_options] = city_province_html_renderer(request=request)
    referer_url = request.session.get("referer_url")
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        address_name = request.POST.get("address_name")
        reciever = request.POST.get("reciever")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        province = request.POST.get("province")
        address = request.POST.get("address")
        postal_code = request.POST.get("postal_code")
        success = True
        error =False
        postal_code_pattern = r'^\d{10}$'
        is_valid = address_name and reciever and phone and city and province and address and postal_code and regex_validator(pattern= r'^(\+98|0)?9\d{9}$', value=phone) and regex_validator(pattern=postal_code_pattern, value=postal_code)
        try:          
            if is_valid:
                Address.objects.create(user=request.user, name=address_name, postal_code=postal_code, address=address, city=city,
                                   province=province, phone=phone, reciever=reciever)
                if referer_url:
                    del request.session["referer_url"]
            else:
                error = True
                success = False                
        except Exception:
            error = True
            success = False
        return JsonResponse({
            "success" : success,
            "error" : error,
            "redirect_url" : referer_url if referer_url else request.build_absolute_uri(reverse("products:index")),
        })
    return render(request, "users/add_address.html", {"error": error, "city_options" : city_options, "province_options" : province_options})


@login_required
def city_ajax_set(request):
    cities = []
    province = request.POST.get("province")
    for city in CostumUser.CITY_CHOICES:
        if city[0][0:3] == province:
            cities.append(city)
    return render(request, "partials/city_set_ajax.html", {"cities": cities})


@login_required
def favourite_products_list(request):
    products = request.user.favourite_products.annotate(
        rating=Avg("comments__rating"))
    return render(request, "users/favourite_products.html", {"products": products})


@login_required
def dashboard_adress(request):
    return render(request, "users/dashboard_adress.html", {"addresses": request.user.addresses.all()})


def address_edit(request, address_id):
    phone_error = None
    postal_code_error = None
    try:
        address = Address.objects.get(pk=address_id)
    except Address.DoesNotExist:
        return render(request, 'generals/404.html')
    if request.method == "POST":
        address_name = request.POST.get("address_name")
        reciever = request.POST.get("reciever")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        province = request.POST.get("province")
        address_adress = request.POST.get("address")
        postal_code = request.POST.get("postal_code")

        if address_name:
            address.name = address_name
        if reciever:
            address.reciever = reciever
        if phone:
            address.phone = str(phone)
            phone_pattern = r'^(\+98|0)?9\d{9}$'
            if not regex_validator(pattern=phone_pattern, value=phone):
                phone_error = True

        if city:
            address.city = city
        if province:
            address.province = province
        if postal_code:
            try:
                int(postal_code)
                address.postal_code = str(postal_code)
            except ValueError:
                postal_code_error = True
        if address_adress:
            address.address = address_adress
        address.save()
        if not phone_error and not postal_code_error:
            return HttpResponseRedirect(reverse("users:dashboard_address"))
    province_option = CostumUser.PROVINCE_CHOICES

    cities = []
    province = address.province

    for city in CostumUser.CITY_CHOICES:
        if city[0][0:3] == province:
            cities.append(city)

    city_options = render_to_string(
        "partials/city_set_ajax.html", {"cities": cities})
    privince_options = render_to_string(
        "partials/province_options.html", {"provinces": province_option, "province": province})
    return render(request, "users/update_address.html", {"address": address, "phone_error": phone_error, "postal_code_error": postal_code_error, "city_options": city_options, "province_options": privince_options})


@login_required
def dashboard_notifications(request):
    return render(request, "users/dashboard_notifications.html", {"notifications": request.user.notifications.all()})


@login_required
def dashbourd_acount(request):
    error_birthday = None
    validation_error = None
    rendered_date = None
    if request.method == "GET":
        rendered_date = (request.user.birthday.strftime(
            "%Y/%m/%d")) if request.user.birthday else None
        form = UserUpdateAccount(instance=request.user, initial={
                                 "birthday": rendered_date})
        [city_options, privince_options] = city_province_html_renderer(request)
    if request.method == "POST":
        data = request.POST.copy()
        [city_options, privince_options] = city_province_html_renderer(request)
        if client_birthday := data.get("birthday"):
            client_birthday = client_birthday.strip()
            if client_birthday and not regex_validator(pattern=r'^(1[3-9]\d{2}|[2-9]\d{3})/(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])$', value=client_birthday):
                error_birthday = "لطفا یک تاریخ با فرمت مناسب وارد کنید"
                form = UserUpdateAccount(data=data, instance=request.user)
            else:
                if client_birthday:
                    birthday_units = client_birthday.split("/")
                    data["birthday"] = "-".join(birthday_units)
                form = UserUpdateAccount(data, instance=request.user)

                if form.is_valid():
                    user = form.save(commit=False)
                    user.province = data["province"]
                    user.city = data["city"]
                    user.save()
                    rendered_date = form.cleaned_data["birthday"].strftime(
                        "%Y/%m/%d") if form.cleaned_data.get("birthday") else None
                    form = UserUpdateAccount(instance=request.user, initial={
                        "birthday": rendered_date})
                    [city_options, privince_options] = city_province_html_renderer(
                        request)
                else:
                    birthday_units = data["birthday"].split(
                        "-") if data.get("birthday") else None
                    rendered_date = "/".join(birthday_units)
                    validation_error = True
        else:
            form = UserUpdateAccount(data=request.POST, instance=request.user)
            if form.is_valid():
                user = form.save(commit=False)
                user.province = data["province"]
                user.city = data["city"]
                user.save()
                rendered_date = form.cleaned_data["birthday"].strftime(
                    "%Y/%m/%d") if form.cleaned_data.get("birthday") else None
                form = UserUpdateAccount(instance=request.user, initial={
                    "birthday": rendered_date})
                [city_options, privince_options] = city_province_html_renderer(
                    request)
    return render(request, "users/dashboard_account.html", {"form": form, "cities": city_options, "provinces": privince_options, "error_birthday": error_birthday, "validation_error": validation_error, "rendered_date": rendered_date})


@login_required
def phone_change_validation(request):
    validation_code = request.session.get("change_phone_validation")
    time_created = request.session.get("change_phone_validation_time")
    form = request.session.get("edit_form")
    uid = request.session["uid"]
    error = None
    now = time.time()
    remaining_time_text = None

    remaining_time = int(180 - (time.time() - time_created))

    if remaining_time > 0:
        minutes = int(remaining_time / 60)
        secounds = int(remaining_time % 60)
        if minutes < 1:
            minutes = f"0{minutes}"
        if secounds < 10:
            secounds = f"0{secounds}"
        remaining_time_text = f"{minutes}:{secounds}"
    if request.method == "POST":
        now = time.time()
        code_units = [request.POST.get("code_unit_1"), request.POST.get("code_unit_2"), request.POST.get(
            "code_unit_3"), request.POST.get("code_unit_4"), request.POST.get("code_unit_5")]
        code = "".join(code_units)
        if code and code == validation_code and (now - time_created) <= 180:
            if form.get("birthday"):
                dates = form.get("birthday").split("/")
                form["birthday"] = "-".join(dates)
            user = CostumUser.objects.filter(pk=uid).update(**form)
            return HttpResponseRedirect(reverse("users:dashboard_account"))
        else:
            error = True
    return render(request, "users/phone_change_validation.html", {"to_phone": form["phone"], "remaining_time": remaining_time, "remaining_time_text": remaining_time_text, "error": error})


@require_POST
def set_city(request):
    success = True
    city_lookup = request.POST.get("city_lookup")
    city_value = request.POST.get("city_value")
    try:
        if request.user.is_authenticated:
            request.user.city = city_lookup
            request.user.save()
        else:
            request.session["city"] = city_value
    except:
        success = False
    return JsonResponse({
        "success": success,
        "city": city_value
    })


@login_required
@require_POST
def edit_phone_phone_entry(request):
    phone_pattern = r'^(\+98|0)?9\d{9}$'
    phone = request.POST.get("phone")
    error = None
    success = True
    user_phone = request.user.phone
    valid_phone = regex_validator(pattern=phone_pattern, value=phone)
    if request.user.is_authenticated:
        if valid_phone:
            if not user_phone == phone:
                if not CostumUser.user_manager.filter(phone=phone).exists():
                    validation_code = str(random.randint(10000, 99999))
                    send_sms_result = send_sms(receptor=user_phone, message=f"کد تایید تغییر شماره {validation_code}")
                    if send_sms_result.get("success"):
                        request.session["generate_for"] = user_phone
                        request.session["validation_code"] = validation_code
                        request.session["validation_code_submit"] = time.time()
                        request.session["new_phone"] = phone
                    else:
                        error = "خطا در وب سرویس پیامکی"
                        success = False
                else:
                    error = "شماره قبلا ثبت شده است!"
                    success = False
            else:
                error = "شماره تلفن جدید نباید با شماره تلفن قبلی برابر باشد"
                success = False
        else:
            error = "شماره تلفن نامعتبر است."
            success = False
    else:
        error = "کاربر نامعتبر"
        success = False
    return JsonResponse({
        "error": error,
        "success": success
    })


@login_required
@require_POST
def edit_phone_validation_previous(reqeust):
    client_validation_code = reqeust.POST.get("validation_code")
    validation_code = reqeust.session.get("validation_code")
    validation_code_set_time = reqeust.session.get("validation_code_submit")
    now = time.time()
    expired = (
        now - validation_code_set_time) >= 120 if validation_code_set_time and now else True
    error = False
    success = True
    if not validation_code == client_validation_code:
        error = "کد تایید صحیح نیست"
        success = False
    if expired:
        error = "کد تایید منقضی شده!"
        success = False
    else:
        new_phone_validation_code = str(random.randint(10000, 99999))
        sms_send_result = send_sms(receptor=reqeust.session.get("new_phone"), message=f"کد تایید شما در پاراسیک شاپ {new_phone_validation_code}")
        if sms_send_result.get("success"):
            reqeust.session["generate_for"] = reqeust.session.get("new_phone")
            reqeust.session["validation_code"] = new_phone_validation_code
            reqeust.session["validation_code_submit"] = now
        else:
            success = False
            error = "مشکل در وب سرویس ارسال پیامک"
  
    return JsonResponse({
        "error": error,
        "success": success,
        "phone": reqeust.session.get("new_phone")
    })


@login_required
@require_POST
def edit_phone_new_phone_validation(request):
    client_validation_code = request.POST.get("validation_code")
    server_validation_code = request.session.get("validation_code")
    validation_code_set_time = request.session.get("validation_code_submit")
    now = time.time()
    expired = (
        now - validation_code_set_time) >= 120 if validation_code_set_time and now else True
    error = False
    success = True
    new_phone = request.session.get("new_phone")

    if not client_validation_code == server_validation_code:
        error = "کد تایید صحیح نیست"
        success = False

    if expired:
        error = "کد تایید منقصی شده است"
        success = False

    else:
        request.user.phone = new_phone
        request.user.save()

    return JsonResponse({
        "error": error,
        "success": success,
        "phone": new_phone,
    })


def generate_new_valiadation_code(request):
    try:
        validation_code = str(random.randint(10000, 99999))
        phone = request.session.get("generate_for")
        sent_from_login_page = request.GET.get("sent_from_login")
        if sent_from_login_page == "true":
            send_sms_result = send_sms(receptor=phone, message=f"کد تایید شما در پاراسیک شاپ {validation_code}")
            if send_sms_result.get("success"):
                request.session["code_gen_time"] = time.time()
                request.session["code"] = validation_code
            else:
                return JsonResponse({
                    "success" : False,
                    "error" : True
                })
        else:
            send_sms_result = send_sms(receptor=phone, message=f"کد تایید شما در پاراسیک شاپ {validation_code}")
            if send_sms_result.get("success"):
                request.session["validation_code"] = validation_code
                request.session["validation_code_submit"] = time.time()
            else:
                return JsonResponse({
                    "error" : True,
                    "success" : False
                })
        return JsonResponse({
            "error": False,
            "success": True
        })
    except KeyError:
        return JsonResponse({
            "error": True,
            "success": False
        })


@require_POST
@login_required
def password_edit_ajax(request):
    previous_password = request.POST.get("previous-password")
    password = request.POST.get("new-password")
    password_confirm = request.POST.get("new-password-confirm")
    error = False
    success = True
    invalid_previous_password = False
    invalid_password_confirm = False
    if request.user.is_authenticated:
        if previous_password and password and password_confirm:
            if request.user.check_password(previous_password):
                if password == password_confirm:
                    request.user.set_password(password)
                    request.user.save()
                else:
                    invalid_password_confirm = True
            else:
                invalid_previous_password = True
        else:
            error = True
            success = False
    else:
        error = True
        success = False
    return JsonResponse({
        "error": error,
        "success": success,
        "invalid_password_confirm": invalid_password_confirm,
        "invalid_previous_password": invalid_previous_password
    })


@login_required
@require_POST
def delete_address(request):
    address_id = request.POST.get("address_id")
    error = False
    success = True
    if address_id and request.user.is_authenticated:
        try:
            address = Address.objects.get(pk=address_id, user=request.user).delete()
        except Address.DoesNotExist:
            error = True
            success = False
    else:
        success = False
        error = True    
    return JsonResponse({
            "success" : success,
            "error" : error
        })

