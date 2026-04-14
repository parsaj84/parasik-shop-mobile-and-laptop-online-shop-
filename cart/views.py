from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import Http404



from products.models import Product, Color
from .cart import Cart, InCartException, UnAvailabeProduct, OutOffCart


def to_thousand_filter(value):
    if value:
        return f"{value:,}"
    else:
        return value

def clear_cart(request):
    cart = Cart(request)
    cart.cart.clear()
    return render(request, "cart/empty_cart_ajax.html")

@require_POST
def add_to_cart(request):
    cart = Cart(request)
    product_id = request.POST.get("product_id")
    color_id = request.POST.get("color_id")
    error = False
    success = True
    html= None
    try:
        product = Product.objects.get(pk=product_id)
        out_off_inventory = False
        if product_id in cart.cart.keys():
            cart.remove(product)
            in_cart = False
        else:
            try:
                color_obj =None
                if color_id:
                    color_obj = product.colors.get(id = color_id)
                cart.add(product, color_obj=color_obj)
                in_cart = True
                html = render_to_string("cart/add_cart_ajax.html", {"product": product,
                                            "item_quantity": cart.cart.get(str(product.pk), {}).get("quantity"),
                                                                        "item_total_price": cart.cart.get(str(product.pk), {}).get("price", 0) * cart.cart.get(str(product.pk), {}).get("quantity", 0),})
            except UnAvailabeProduct:
                in_cart = False
            except Color.DoesNotExist:
                error = True
                success = False    
            out_off_inventory = True
    except Product.DoesNotExist:
        error =True
        success = False

    context = {
        "total_items": cart.item_count(),
        "in_cart": in_cart,
        "item_quantity": cart.cart.get(str(product.pk), {}).get("quantity"),
        "unavailable": out_off_inventory,
        "success": success,
        "error" : error,
        "html" : html,
        "final_price": to_thousand_filter(cart.total_price()),
    }
    return JsonResponse(context)

@require_POST
def add_to_cart_detail(request):
    html = None
    out_off_inventory = False
    success = True
    in_cart = False
    cart = Cart(request)
    if request.POST.get("product_id"):
        product = Product.objects.prefetch_related("colors").get(pk=request.POST.get("product_id"))
        if not str(product.pk) in cart.cart.keys():
            try:
                color_id = request.POST.get("color_id")
                color_obj = None
                if color_id:
                    color_obj = product.colors.get(pk=color_id)
                cart.add(product, color_obj=color_obj)
            except UnAvailabeProduct:
                out_off_inventory = True
                return JsonResponse({"success": True, "unavailable": out_off_inventory})

            html = render_to_string("cart/add_cart_ajax.html", {"product": product,
                                    "item_quantity": cart.cart.get(str(product.pk), {}).get("quantity"),
                                                                "item_total_price": cart.cart.get(str(product.pk), {}).get("price", 0) * cart.cart.get(str(product.pk), {}).get("quantity", 0),
                                                                })
            context = {
                "total_items": cart.item_count(),
                "in_cart": in_cart,
                "item_quantity": cart.cart.get(str(product.pk), {}).get("quantity"),
                "unavailable": out_off_inventory,
                "item_total_price": to_thousand_filter(cart.cart[str(product.pk)]["price"] * cart.cart[str(product.pk)]["quantity"]),
                "success": True,
                "html": html,
                "final_price": to_thousand_filter(cart.total_price()),
            }
        else:
            success = False
            in_cart = True
            context = {
                "success": success,
                "in_cart": in_cart,
                "html": html,
            }

    return JsonResponse(context)

@require_POST
def remove_from_cart(request):
    send_from_detail = request.POST.get("send_from_detail")
    cart = Cart(request)
    product_id = request.POST.get("product_id")
    success = None
    in_cart = False
    if str(product_id) in cart.cart.keys():
        cart.remove(product=Product.objects.get(pk=product_id))
        success = True
        in_cart = True
    else:
        in_cart = False
        success = False
    context = {
        "html": False,
        "total_items": cart.item_count(),
        "in_cart": in_cart,
        "success": success,
        "final_price": to_thousand_filter(cart.total_price()),
        "product_id": str(product_id)
    }
    if send_from_detail and not cart.cart:
        context["html"] = render_to_string(
            template_name="cart/empty_cart_ajax.html")
    return JsonResponse(context)

@require_POST
def increase_cert_item(request):
    cart = Cart(request)
    product_id = request.POST.get("product_id")
    product = Product.objects.get(pk=product_id)
    out_of_inventory = False
    success = None
    if str(product_id) in cart.cart.keys():
        try:
            cart.increase(product)
            success = True
            out_of_inventory = False
        except UnAvailabeProduct:
            out_of_inventory = True
            success = True
        except BaseException:
            success = False
        context = {
            "item_quantity": cart.cart.get(str(product_id), {}).get("quantity"),
            "success": success,
            "unavailable": out_of_inventory,
            "item_total_price": to_thousand_filter(cart.cart.get(str(product_id), {}).get("price", 0) * cart.cart.get(str(product_id), {}).get("quantity", 0)),
            "final_price": to_thousand_filter(cart.total_price()),
            "product_id": str(product.pk)

        }

    return JsonResponse(context)

@require_POST
def decrease_from_cart(request):
    send_from_detail = request.POST.get("send_from_detail")
    cart = Cart(request)
    product_id = request.POST.get("product_id")
    out_off_cart = False
    success = True
    if str(product_id) in cart.cart.keys():
        try:
            cart.decrease(product=Product.objects.get(pk=product_id))
            success = True
        except OutOffCart:
            out_off_cart = True
        except BaseException:
            success = False

    context = {
        "html":False,
        "out_off_cart": out_off_cart,
        "success": success,
        "item_quantity": cart.cart[str(product_id)]["quantity"] if cart.cart.get(str(product_id)) else 0,
        "total_items": cart.item_count(),
        "item_total_price": to_thousand_filter(cart.cart.get(str(product_id), {}).get("price", 0) * cart.cart.get(str(product_id), {}).get("quantity", 0)),
        "final_price": to_thousand_filter(cart.total_price()),
        "product_id" : str(product_id)


    }
    if send_from_detail and not cart.cart:
           context["html"] = render_to_string(
            template_name="cart/empty_cart_ajax.html")
    return JsonResponse(context)

def cart_detail(request):
    cart = Cart(request)
    if not cart.cart:
        return render(request, "cart/empty_cart.html")
    else:
        return render(request, "cart/cart_detail.html")

# Create your views here.
