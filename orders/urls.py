from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", view=views.checkout, name="checkout"),
    path("checkout-process/", views.checkout_process, name="checkout_process"),
    path("payment/", views.payment, name="payment"),
    path("off-code-ajax/", views.off_code_ajax, name="off_code_ajax"),
    path("order-list/", views.order_list , name="order_list"),
    path("factor/<int:order_id>", views.factor_gen, name="factor_pdf"),
    path("edit-order/<int:order_id>/", view=views.order_edit, name="order_edit"),
    path("edit-order-form/", view=views.order_edit_ajax, name="order_edit_ajax"),
    path("refrall-request-process/", view=views.refrall_request_process, name="refrall_request_process"),
    path("refrall-request-form/", view=views.refrall_request_form, name="refrall_request_form"),
    path("payment-final/", view=views.fake_payment, name="fake_payment"),

]
