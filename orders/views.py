from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone



import json
from datetime import timedelta
from jdatetime import date


from users.models import Address, CostumUser
from cart.cart import Cart
from .forms import OrderForm
from .models import Order, Item, OffCode, RefrallRequest,Transcation
from products.views import to_thousand_filter

from weasyprint import HTML
import jdatetime
import pytz
import random


def get_delivery_date(request,order=None):
    if order and order.date_delivery:
        return order.date_delivery
    else:
        now = timezone.now().astimezone(pytz.timezone("Asia/Tehran")).date()
        duration_days = 3 if request.user.province == "thr" else 5
        delivery_date_gregorian = now + timedelta(days=duration_days)
        return jdatetime.date.fromgregorian(date=delivery_date_gregorian, locale="fa_IR")



@login_required
def checkout(request):
    cart = Cart(request)
    if cart.cart:
        if request.user.addresses.exists():
            form = OrderForm()
            addresses = request.user.addresses.all()
            pishtaz_post_rate = to_thousand_filter(int(cart.post_price() *1.5))
            manual_post_price = to_thousand_filter(int(cart.post_price() * 1.25))
            estimated_delivery_date = get_delivery_date(request)
        else:
            request.session["referer_url"] = request.build_absolute_uri(reverse("orders:checkout"))
            return HttpResponseRedirect(reverse("users:add_address"))
    else:
        return HttpResponseRedirect(reverse("products:product_list"))
    return render(request, "orders/checkout.html", {"form": form,"estimated_delivery_date" : estimated_delivery_date ,"addresses": addresses, "manual_post_price" : manual_post_price, "pishtaz_post_rate" : pishtaz_post_rate})


@csrf_exempt
@require_POST
def checkout_process(request):
    body = request.body.decode('utf-8')
    raw_data = json.loads(request.body)
    data = raw_data.get("data", {})
    post_type = raw_data.get("post_type")
    post_rate = 1.25 if post_type == "MN" else 1.5
    form = OrderForm(data)
    cart = Cart(request)
    if form.is_valid() and post_type:
        address = request.user.addresses.get(pk=data["address"])
        order = form.save(commit=False)
        order.post_type = post_type
        order.address = address
        order.buyer = request.user
        order.total_price = cart.total_price()
        order.send_price = cart.post_price() * post_rate
        order.save()
        for item in cart:
            product_price = item["product"].price_after_off if item["product"].off else item["product"].price
            item_color = item.get("color", {})
            color_map = {"name" : item_color.get("name") , "item_color_style" : item_color.get("style_color_class")} if item_color else None
            color_map_json = json.dumps(color_map) if color_map else None
            item = Item.objects.create(order=order,
                                       product=item["product"], price=product_price, weight=item["product"].weight, quantity=item["quantity"], color=color_map_json)
        request.session["created_order_id"] = order.pk
        request.session["base_price"] = cart.total_price()
        if request.session.get("cart"):
            del request.session["cart"]
            cart.cart.clear()
        return JsonResponse({"redirect_url" : reverse("orders:payment")})
    else:
        error = True
        return JsonResponse({"error": error})
    
@login_required
def payment(request):
    base_price = request.session.get("base_price")
    try:
        order = Order.objects.get(pk=request.session.get("created_order_id"))
    except Order.DoesNotExist:
        return render(request, 'generals/404.html')
    total_price_dereament = sum(off_code_object.price_decreament for off_code_object in order.off_codes.all())
    order_has_off = True if request.session.get("order_has_off") else False
    estimated_delivery_date = get_delivery_date(request)
    return render(request, "orders/payment.html", {"order_has_off" : order_has_off,"estimated_delivery_date" : estimated_delivery_date,"order" : order,"base_price" : base_price ,"off_decreament" : total_price_dereament})


@login_required
@require_POST
def off_code_ajax(request):
    success = True
    error_off_code_none = False
    error_code_invalid = False
    final_price = None
    off_type = None
    error_not_reached_limit = False
    price_dereament = None
    try:
       order = Order.objects.prefetch_related("off_codes").get(pk=request.session.get("created_order_id"))
       off_code = request.POST.get("off-code")
       off_code_obj = OffCode.objects.get(code = off_code)
       off_type = off_code_obj.off_type
       if off_code_obj in request.user.off_codes.all():
            if off_type == "PRDC":
                if off_code_obj.min_price <= order.total_price: 
                    order.total_price = order.total_price - off_code_obj.price_decreament
                    order.off_codes.add(off_code_obj)
                    request.user.off_codes.remove(off_code_obj)
                    final_price = order.total_price + order.send_price
                    price_dereament = sum(off_code_object.price_decreament for off_code_object in order.off_codes.all())
                    order.save()
                else:
                    error_not_reached_limit =True
            if off_type == "FRSE":
                order.send_price = 0
                request.user.off_codes.remove(off_code_obj)
                order.off_codes.add(off_code_obj)
                order.save()
                final_price = order.total_price + order.send_price
       else:
           error_code_invalid = True
           success = False
    except OffCode.DoesNotExist or Order.DoesNotExist:
        error_off_code_none = True
        success = False
    context = {
        "error_not_reached_limit" : error_not_reached_limit,
        "error_invalid_code" : error_code_invalid,
        "error_off_code_none" : error_off_code_none,
        "success" : success,
        "off_type" : off_type,
        "price_decreament" : to_thousand_filter(price_dereament), 
        "final_price" : to_thousand_filter(final_price)
    }
    return JsonResponse(context)



@login_required
def order_list(request):
    orders = Order.objects.order_by("-date_created").filter(buyer=request.user)
    return render(request , "orders/dashboard_order_list.html" , {"orders" : orders})


@login_required
def order_edit(reqeust, order_id):
    try:
        order = Order.objects.prefetch_related("off_codes").get(id = order_id, buyer = reqeust.user)
        form = OrderForm(instance=order)
        addresses = Address.objects.filter(user = reqeust.user)
        total_decreament = sum(off_code.price_decreament for off_code in order.off_codes.filter(off_type = "PRDC"))
        estimated_delivery_date = get_delivery_date(reqeust,order=order)
        return render(reqeust, "orders/edit_order.html",{"order" : order,"estimated_delivery_date" : estimated_delivery_date,"form" : form,"addresses": addresses, "price_decreament" : total_decreament})
    except Order.DoesNotExist:
        return render(reqeust, "generals/404.html")
    
@login_required
@require_POST
def order_edit_ajax(reqeust):
    order_id = reqeust.POST.get("order_id")
    address_id = reqeust.POST.get("address")
    success = True
    error = False
    delivery_error = False
    error_invalid_information = False
    try:
        address = Address.objects.get(pk=address_id)
        order = Order.objects.get(pk=order_id)
        if order.status == "DELIVERY":
            success = True
            delivery_error = True
        else:
            form = OrderForm(data=reqeust.POST, instance=order)
            if form.is_valid():
                order = form.save(commit=False)
                order.address = address
                order.save()
            else:
                success = True
                error_invalid_information = True
    except Order.DoesNotExist or Address.DoesNotExist:
        error = True
        success = False
    context = {
        "success" : success,
        "error" : error,
        "error_invalid_information" : error_invalid_information,
        "delivery_error" : delivery_error,
    }
    return JsonResponse(context)


@login_required
def factor_gen(request, order_id):
    try:
        order = Order.objects.get(id = order_id)
        if order.buyer == request.user:
           factor_html = render_to_string("orders/factor_pdf.html", {"order" : order})
           factor_pdf = HTML(string=factor_html).write_pdf()
           response = HttpResponse( content=factor_pdf,content_type="application/pdf")
           response["Content-Dispostion"] = f"attachment; filename=factor-{order.pk}.pdf"
           return response
        else:
             return HttpResponseForbidden()
    except Order.DoesNotExist:
        return render(request, "generals/404.html")



@require_POST
def refrall_request_process(request):
    if request.user.is_authenticated:
        item_id = request.POST.get("item_id")
        success = True
        error = False
        refrall_before_send = False
        refrall_after_send = False
        can_refrall = False
        deleted_order= False
        redirect_url = None
        refall_form_html = None
        try:
            item = Item.objects.select_related("order").get(pk=item_id)
            order = item.order
            if order.is_paid:
                if order.status == "PRC":
                    refrall_before_send = True
                    decreament = (item.price if item.price else item.product.price_after_off) * item.quantity
                    order.total_price -= decreament
                    RefrallRequest.objects.create(item=item, user=request.user, reason="انصراف از خرید", is_accepted = True)
                    item.delete()
                    if order.items.exists():
                        order.save()
                    else:
                        deleted_order = True
                        redirect_url = reverse(viewname="orders:order_list")
                        order.delete()
                if order.status == "DELIVERY":
                    can_refrall = (timezone.now().astimezone(pytz.timezone("Asia/Tehran")).date() - order.date_given_to_post.togregorian()).days <= 10
                    refrall_after_send = True
                    if can_refrall:
                        refall_form_html = render_to_string( "orders/partials/refrall_form.html", {"item" : item})
        
        except Item.DoesNotExist:
            success = False
            error = True
    else:
        return JsonResponse({
            "error" : True,
            "success" : False
        })
    return JsonResponse({
        "success" : success,
        "error" : error,
        "refrall_before_send" : refrall_before_send,
        "refrall_after_send" : refrall_after_send,
        "can_refrall" :can_refrall,
        "html" : refall_form_html,
        "order_new_price" : to_thousand_filter(order.total_price + order.send_price) if not deleted_order else 0,
        "items_new_price" : to_thousand_filter(sum(item.price * item.quantity for item in order.items.all()))  if not deleted_order else 0,
        "deleted_order" : deleted_order,
        "redirect_url" : redirect_url,
        })


@require_POST
def refrall_request_form(request):
    if request.user.is_authenticated:
        file= request.FILES.get("item_img")
        success= True
        error = False
        item_id = request.POST.get("item_id")
        limit_size = 2 * 1024 * 1024
        try:
            item = Item.objects.get(pk=item_id)
            refrall_reqeust_exists = True if RefrallRequest.objects.filter(item=item).exists() else False
            can_refrall = item.order.status == "DELIVERY" and (timezone.now().astimezone(pytz.timezone("Asia/Tehran")).date() - item.order.date_given_to_post.togregorian()).days <= 10 if item.order.date_given_to_post  else False
            if file and file.size <= limit_size:
                if not refrall_reqeust_exists:
                    if can_refrall:
                        RefrallRequest.objects.create(user=request.user , item=item, reason=request.POST.get("resoen"), image=file)    
            else:
                error=True
                success =False
        except Item.DoesNotExist:
            error = True
            success = False
        return JsonResponse({
            "error" : error,
            "success" : success,
            "can_refrall" : can_refrall,
            "refrall_reqeust_exists" : refrall_reqeust_exists,

        })
    else:
        return JsonResponse({
            "error" : True,
            "success" : False
        })


@login_required
def fake_payment(request):
    order_id = request.session.get("created_order_id")
    if order_id:
        del request.session["created_order_id"]
    if not order_id:
        return HttpResponseRedirect(reverse("products:index"))
    try:
        order = Order.objects.get(id = order_id)
        tranaction = Transcation.objects.create(order=order, sender=request.user, price=order.total_price + order.send_price)
        tracking_id = str(random.randint(10000000,99999999))
        while Order.objects.filter(tracking_id = tracking_id).exists():
            tracking_id = str(random.random(10000000,99999999))
        order.tracking_id = tracking_id
        order.is_paid=True
        order.status = ""
        order.save(saved_from_fake_payment=True)
        return render(request, "orders/successfull_payment.html", {"transaction" : tranaction, "order" : order})
    except Order.DoesNotExist:
        return render(request, "generals/404.html")