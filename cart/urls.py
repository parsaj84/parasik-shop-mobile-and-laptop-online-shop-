from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("add-to-cart-detail/", views.add_to_cart_detail, name="add_to_cart_detail"),
    path("remove-from-cart/", views.remove_from_cart, name="remove_from_cart"),
    path("increase-item-cart/", views.increase_cert_item, name="increase_cart_item"),
    path("decrease-from-cart/", views.decrease_from_cart, name="decrease_from_cart"),
    path("cart-detail/", views.cart_detail, name="cart_detail"),
    path("clear-cart/", views.clear_cart, name="clear_cart")

]