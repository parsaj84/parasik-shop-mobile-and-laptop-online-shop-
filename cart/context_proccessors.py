from .cart import Cart

def cart(request):
    return {"cart" : Cart(request=request)}

def cart_product_ids(request):
    return {"cart_product_ids" : [item["product"].id for item in Cart(request)]}