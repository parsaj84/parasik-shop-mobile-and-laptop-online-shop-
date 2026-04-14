from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST, require_safe
from django.contrib.postgres.search import TrigramSimilarity
from django.http import HttpResponseNotFound
from django.db.models import Max, Min, Q, Case, Avg, Count
from django.http import Http404
from .models import Comment
from django.contrib import messages
from django.http import JsonResponse
from cart.cart import Cart
from django.template.loader import render_to_string
from django.db.models import Count

from cart.views import to_thousand_filter


import pytz
import json


from datetime import timedelta, datetime
from .models import Category, Slider, Product, AmazingOfferMain, UserOponionComment
from article.models import Post


def index(request):
    exist = True
    sliders = Slider.objects.all()
    offer = AmazingOfferMain.objects.prefetch_related("products").first()
    if offer:
        products = Product.objects.filter(amazing_offer__in=[offer]).annotate(
            rating=Avg("comments__rating"))
    now_utc = timezone.now()
    tehran_tz = pytz.timezone("Asia/Tehran")
    now_tehran = now_utc.astimezone(tehran_tz)
    if now_tehran > offer.datetime:
        exist = False
    most_popular_products = Product.objects.annotate(popularity=Count("favourite_by")).order_by("-popularity")[0:8]
    most_selled_products = Product.objects.annotate(selled=Count("in_orders", filter=Q(in_orders__order__is_paid=True))).order_by("-selled")[0:8]
    posts = Post.objects.all()[0:7]
    differance = offer.datetime - now_tehran
    hours = int(differance.seconds / 3600)
    minutes = int((differance.seconds % 3600) / 60)
    secounds = int((differance.seconds % 3600) % 60)
    return render(request, "products/index.html", {"exists": exist, "sliders": sliders, "hours": hours, "minutes": minutes, "secounds": secounds, "products": products, "offer": offer, "most_selled_products" :most_selled_products,"most_popular_products" : most_popular_products ,"posts" : posts})


def product_list(request, product_id=None, product_slug=None, category_slug=None, slider_id=None, amazing_id=None):
    products = Product.objects.all()
    category = None
    slider = None
    cat_id = None
    category_is_needed = True
    if amazing_id:
        try:
            amazing_offer = AmazingOfferMain.objects.prefetch_related(
                "products").get(pk=amazing_id)
            products = amazing_offer.products.all()
            category_is_needed = False
        except AmazingOfferMain.DoesNotExist:
            return render(request, 'generals/404.html')
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category)
        category_is_needed = False
    if slider_id:
        try:
            slider = Slider.objects.get(id=slider_id)
        except Slider.DoesNotExist:
            return render(request, 'generals/404.html')
        products = slider.products.all()
        category_is_needed = False
    if product_id and product_slug:
        try:
            product = Product.objects.prefetch_related(
                "category").get(pk=product_id, slug=product_slug)
            product_cat = product.category.all()
            products = Product.objects.filter(
                category__in=product_cat).annotate(similarity=Count("category")).order_by("similarity").exclude(pk=product_id).distinct()
            category_is_needed = False
        except Product.DoesNotExist:
            return render(request, 'generals/404.html')
    max_range = products.aggregate(max_price=Max("price"))
    min_range = products.aggregate(min_price=Min("price"))
    page_num = request.GET.get("page")
    page = page_num
    page_num = request.GET.get("page")
    cat_id = request.GET.get("cat_id")
    inventory = request.GET.get("inventory")
    today_delivery = request.GET.get("today_delivery")
    order_by = request.GET.get("order_by")
    client_search = request.GET.get("search")
    inventory_ = False
    today_delivery_ = False
    seller_send_ = False
    attendent_buy = False
    order_by_min_price = False
    order_by_favourite = False
    order_by_max_price = False
    order_by_sale = False
    distance_from_left = None
    distance_from_right = None
    min_range_ajax = None
    max_range_ajax = None

    if today_delivery == "true":
        products = products.filter(today_delivery=True)
        today_delivery_ = True

    if cat_id:
        try:
            ajax_category = Category.objects.get(pk=cat_id)
            products = products.filter(category=ajax_category)
        except Category.DoesNotExist:
            return render(request, 'generals/404.html')
    if inventory == "true":
        products = products.filter(inventory__gte=1)
        inventory_ = True
    if request.GET.get("seller_send") == "true":
        products = products.filter(seller_delivary=True)
        seller_send_ = True
    if request.GET.get("attendant_buy") == "true":
        products = products.filter(attendtent_sale=True)
        attendent_buy = True
    if request.GET.get("max_price") and request.GET.get("min_price"):
        products = products.filter(price__gte=request.GET.get(
            "min_price"), price__lte=request.GET.get("max_price"))
        q_max_price = max_range.get("max_price")
        q_min_price = min_range.get("min_price")
        f_max_price = int(request.GET.get("max_price"))
        f_min_price = int(request.GET.get("min_price"))
        base = q_max_price - q_min_price
        distance_from_right = ((q_max_price - f_max_price) / base) * 100
        distance_from_left = ((f_min_price - q_min_price) / base) * 100
        max_range_ajax = {"max_price": request.GET.get("max_price")}
        min_range_ajax = {"min_price": request.GET.get("min_price")}
    if order_by:
        if order_by == "favorite":
            products = products.annotate(in_favourite_count=Count(
                "favourite_by")).order_by("-in_favourite_count")
            order_by_favourite = True
        if order_by == "sale":
            products = products.annotate(
                ordered=Count("in_orders", filter=Q(in_orders__order__is_paid=True))).order_by("-ordered")
            order_by_sale = True
        if order_by == "min_price":
            products = products.order_by("price_after_off")
            order_by_min_price = True
        if order_by == "max_price":
            products = products.order_by("-price_after_off")
            order_by_max_price = True
    if client_search:
        products = products.annotate(similarity=TrigramSimilarity("name", client_search)).filter(
            similarity__gt=0.1).order_by("-similarity")
        category_is_needed = False
    count = products.count()
    paginator = Paginator(products, 4)
    try:
        products = paginator.page(page_num)
    except EmptyPage:
        paroducts = paginator.page(1)
        page = 1
    except PageNotAnInteger:
        products = paginator.page(1)
        page = 1
    query_params = request.GET.copy()
    if "page" in query_params:
        del query_params["page"]
    no_cat_filter = False
    if slider or category:
        no_cat_filter = True
    return render(request, "products/productl.html", {"count": count, "selected_min_range": min_range_ajax, "selected_max_range": max_range_ajax, "right": distance_from_right, "left": distance_from_left, "order_by_favourite": order_by_favourite, "order_by_sale": order_by_sale, "order_by_max_price": order_by_max_price, "order_by_min_price": order_by_min_price, "oreder_by": order_by, "attendent_buy": attendent_buy, "today_delivery": today_delivery_, "inventory": inventory_, "seller_send": seller_send_, "cat_id": cat_id, "no_cat_filter": no_cat_filter, "page": page, "min": min_range, "max": max_range,  "slider": slider, "products": products, "category_is_needed": category_is_needed, "query_params": query_params, "slider_id": slider_id, "cat_slug": category_slug, "amazing_offer_id": amazing_id})


def search_ajax(request):
    client_search = request.GET.get("search")
    result = None
    if client_search:
        result = Product.objects.annotate(similarity=TrigramSimilarity(
            "name", client_search)).filter(similarity__gt=0.1).order_by("-similarity")[:4]
       
    return render(request, "products/search_result_ajax.html", {"query": client_search, "result": result})


def search(request):
    query = request.GET.get("search")
    page_number = None
    page = None
    count = None
    result = None
    if query:
        result = Product.objects.annotate(similarity=TrigramSimilarity("name", query)).filter(
            similarity__gt=0.1).order_by("similarity")
        if result:
            count = result.count()
            try:
                paginator = Paginator(result, 6)
                page_number = request.GET.get("page", 1)
                page = page_number
                result = paginator.page(page_number)
            except EmptyPage:
                result = None
    return render(request, "products/productl.html", {"query": query, "page": page_number, "count": count, "products": result})


def product_detail(request, product_id, product_slug):
    product_brand = None
    product_sub_cat = None
    colors_map = None
    cart = Cart(request=request)
    quantity = cart.cart.get(str(product_id), {}).get("quantity")
    try:
        product = Product.objects.prefetch_related("comments", "in_orders", "category", "colors").annotate(rating=Avg("comments__rating")).get(
            pk=product_id, slug=product_slug)
        price_after_off = product.price_after_off
        product_category = product.category.all()
        related_products = Product.objects.filter(category__in=product_category).annotate(
            rating=Avg("comments__rating")).distinct().exclude(pk=product.pk)[0:7]
        product_comments = product.comments.filter(
            status="PB").order_by('-date_created')
        rating = product.rating if product.rating else 0
        if product.has_colors:
            colors_map = json.dumps({item["style_class"] : item["name"] for item in product.colors.values("style_class", "name")})

        product.save()
    except Product.DoesNotExist:
        return render(request, 'generals/404.html')
    return render(request, "products/productd.html", {"product": product, "colors_map": colors_map, "product_total_price": cart.cart.get(str(product_id), {}).get("price", 0) * cart.cart.get(str(product_id), {}).get("quantity", 0), "product_price": product.price, "price_after_off": price_after_off, "qunatity_in_cart": quantity, "sub_cat_grand": product_sub_cat, "brand": product_brand, "rating": int(rating), "comments": product_comments, "related_products": related_products})


@require_POST
def comment_submiter(request, product_id):
    error = None
    success = None
    comment = None
    is_authenticated = request.user.is_authenticated
    if is_authenticated:
        raw_data = dict(request.POST)
        del raw_data["csrfmiddlewaretoken"]
        usable_data = {key: value[0] for key, value in raw_data.items()}
        suggest_to_buy = usable_data.pop("suggest")
        try:
            product = Product.objects.get(pk=product_id)
            comment = Comment.objects.create(
                product=product, user=request.user, sugest_to_buy=True if suggest_to_buy == "true" else False, **usable_data)
            success = True
            error = False
        except Product.DoesNotExist:
            error = True
            success = False
    else:
        error = False
        success = True

    return JsonResponse({"error": error, "success": success, "is_authenticated": is_authenticated})


def products_ajax_handler(request):
    page_num = request.GET.get("page")
    cat_id = request.GET.get("cat_id")
    inventory = request.GET.get("inventory")
    today_delivery = request.GET.get("today_delivery")
    order_by = request.GET.get("order_by")
    products = Product.objects.all()
    client_search = request.GET.get("search")
    slider_id = request.GET.get("slider_id")
    cat_slug = request.GET.get("cat_slug")
    amazing_offer_id = request.GET.get("amazing_id")
    if cat_slug and cat_slug != "None":
        
        category = Category.objects.prefetch_related(
            "products").get(slug=cat_slug)
        products = category.products.all()
    if slider_id and slider_id != "None":
        slider = Slider.objects.prefetch_related("products").get(pk=slider_id)
        products = slider.products.all()
    if amazing_offer_id and amazing_offer_id != "None":
        amazing_offer = AmazingOfferMain.objects.prefetch_related(
            "products").get(pk=amazing_offer_id)
        products = amazing_offer.products.all()

    if today_delivery == "true":
        products = products.filter(today_delivery=True)
    if cat_id:
        try:
            category = Category.objects.get(pk=cat_id)
            products = products.filter(category=category)
        except Category.DoesNotExist:
            return HttpResponseNotFound()
    if inventory == "true":
        products = products.filter(inventory__gte=1)
    if request.GET.get("seller_send") == "true":
        products = products.filter(seller_delivary=True)
    if request.GET.get("attendant_buy") == "true":
        products = products.filter(attendtent_sale=True)
    if request.GET.get("max_price") and request.GET.get("min_price"):
        products = products.filter(price__gte=request.GET.get(
            "min_price"), price__lte=request.GET.get("max_price"))
    if order_by:
        if order_by == "favorite":
            products = products.annotate(in_favourite_count=Count(
                "favourite_by")).order_by("-in_favourite_count")
        if order_by == "sale":
            products = products.annotate(
                ordered=Count("in_orders", filter=Q(in_orders__order__is_paid=True))).order_by("-ordered")
        if order_by == "min_price":
            products = products.order_by("price_after_off")
        if order_by == "max_price":
            products = products.order_by("-price_after_off")
    if client_search:
        products = products = products.annotate(similarity=TrigramSimilarity("name", client_search)).filter(
            similarity__gt=0.1).order_by("-similarity")
    count = products.count()
    paginator = Paginator(products, 4)
    try:
        products = paginator.page(page_num)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(1)

    template = render_to_string(request=request, template_name="products/result_ajax.html",
                                context={"count": count, "products": products, "page": page_num})
    return JsonResponse({"template": template, "count": count})


@require_POST
def user_oponion_submit(request):
    is_authenticated = request.user.is_authenticated
    error = False
    success = True
    is_usefull = True if request.POST.get("is_usefull") == "true" else False
    if is_authenticated:
        try:
            comment = Comment.objects.get(pk=request.POST.get("comment_id"))
            if UserOponionComment.objects.filter(comment_to=comment, user_from=request.user).exists():
                user_oponion = UserOponionComment.objects.get(
                    comment_to=comment, user_from=request.user)
                if user_oponion.is_usefull == is_usefull:
                    pass
                else:
                    user_oponion.is_usefull = is_usefull
                    user_oponion.save()
            else:
                user_oponion = UserOponionComment.objects.create(
                    comment_to=comment, user_from=request.user, is_usefull=is_usefull)
        except Comment.DoesNotExist:
            success = False
            error = True
    else:
        return JsonResponse({
            "success": True,
            "error": False,
            "is_authenticated": is_authenticated
        })
    return JsonResponse({
        "success": success,
        "error": error,
        "is_authenticated": is_authenticated,
        "yes_count": comment.user_oponions.filter(is_usefull=True).count(),
        "no_count": comment.user_oponions.filter(is_usefull=False).count(),
    })


def about_us(request):
    return render(request, "products/about_us.html")

def contact_us(request):
    return render(request, "products/contact_us.html")

def frequent_questions(request):
    return render(request,"products/frequent_q.html")