from django.urls import path
from django.shortcuts import render


from . import views

app_name = "products"

def handler404(request,exception):
    return render(request, "generals/404.html",status=404)

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.product_list, name="product_list"),
    path("products-slider/<int:slider_id>/",
         views.product_list, name="product_by_slider"),
    path("amazing-offer/<int:amazing_id>/", view=views.product_list, name="amazing_offer"),
    path("products-by-category/<str:category_slug>/",
         views.product_list, name="product_by_category"),
    path("search-ajax/", views.search_ajax, name="search_ajax"),
    path("search/", views.search, name="search_complete"),
    path("product-detail/<int:product_id>/<str:product_slug>/",
         views.product_detail, name="product_detail"),
    path("comment-submiter/<int:product_id>/",
         views.comment_submiter, name="comment_submiter"),
    path("related-products/<int:product_id>/<str:product_slug>/",
         views.product_list, name="related_products_list"),
    path("products-ajax-handler/", views.products_ajax_handler, name="products_ajax_handler"),
     path("user-oponion-submit/", views.user_oponion_submit, name="user_oponion_submit"),
     path("contact-us/", view= views.contact_us, name="contact_us"),
     path("about-us/", view=views.about_us, name="about_us"),
     path("questions/", view=views.frequent_questions, name="frequent_questions")
]
