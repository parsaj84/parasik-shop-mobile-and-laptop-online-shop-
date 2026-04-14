from django import template

from ..models import UserOponionComment

register = template.Library()


@register.filter(name="secound_in_query")
def secound_in_query(value):
    if len(value) >= 2:
        return value[1]
    return None


@register.filter(name="in_cart")
def in_cart(value, cart):

    return str(value.pk) in cart.cart.keys()


@register.filter(name="thousands_separator")
def thousands_separator(num):
    try:
        return f"{int(num):,}"
    except (ValueError, TypeError):
        return num


@register.filter(name="check_cat")
def check_cat(value, cat):
    is_true =False
    if value:
        is_true = True if int(value) == cat.pk else False
    return is_true

@register.filter(name="check_is_buyer")
def check_is_buyer(product, user):
    product_in_orders = product.in_orders.select_related("order").all()
    is_buyer = False
    for item in product_in_orders:
        if user == item.order.buyer and item.order.is_paid:
            is_buyer = True
            break
    return is_buyer

@register.filter(name="comment_user_oponion_process")
def comment_user_oponion_process(comment):
    return {"was_usefull" : comment.user_oponions.filter(is_usefull=True).count(), "was_not_usefull" : comment.user_oponions.filter(is_usefull=False).count()}


@register.simple_tag(name="check_if_current_color")
def check_if_current_color(color_obj, cart, product):
    product_id = str(product.pk)
    if cart and str(product_id) in cart.keys():
        cart_item = cart.get(product_id)
        color = cart_item.get("color")
        if color:
            return color.get("id") == color_obj.id
    return None
        

@register.filter(name="get_color")
def get_color(product, cart_obj):
    cart_item =cart_obj.cart.get(str(product.id))
    if cart_item:
        color = cart_item.get("color")
        if color:
            return color.get("name")
