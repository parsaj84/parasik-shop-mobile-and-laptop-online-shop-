from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count


from .models import Post, Category


def posts_list(request, category_slug=None, pid=None):
    posts = Post.acp_manage.all().annotate(views = Count("user_viewed")).order_by("-views", "-date_created")
    cat_ids_list = request.GET.get("cat_id").split(
        ",") if request.GET.get("cat_id") else []
    order_option = request.GET.get("order")
    category = None
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            posts = posts.filter(categories__in=[category])
        except Category.DoesNotExist:
            return render(request, "generals/404.html")
     
    if pid:
        try:
            post = Post.objects.prefetch_related("categories").get(pk=pid)
            categories = post.categories.all()
            posts = posts.exclude(pk=pid).filter(
                categories__in=categories).annotate(similarity= Count("categories")).order_by("-similarity").distinct()
        except Post.DoesNotExist:
            return render(request, "generals/404.html")
    if cat_ids_list:
        for cat_id in cat_ids_list:
            posts = posts.filter(categories__id__in=[cat_id])
    if order_option:
        if order_option == "newest":
            posts = posts.order_by("-date_created")
        if order_option == "most_viewed":
            posts = posts.order_by("-views") 
    related_categories = Category.objects.prefetch_related("posts").filter(posts__in=posts).exclude(sub_cat=None).distinct()
    query_params = request.GET.copy()
    if "page" in query_params:
        del query_params["page"]
    paginator = Paginator(posts, 2)
    page_obj = request.GET.get("page")
    posts_count = posts.count()
    try:
        posts = paginator.page(page_obj)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(1)
    return render(request, "blog/postl.html", {"posts": posts, "related_categories": related_categories, "category": category, "pid": pid if pid else "", "count": posts_count, "fitlered_cat_ids": cat_ids_list, "query_params": query_params, "order_option": order_option})


def article_detail(request, post_id, post_slug):
    try:
        post = Post.objects.prefetch_related(
            "categories", "user_viewed").get(id=post_id, slug=post_slug)
        post_categories = post.categories.all()
        if not post.status == "ACP":
            return render(request, "generals/404.html")
        if request.user.is_authenticated and not request.user in post.user_viewed.all():
            post.user_viewed.add(request.user)
        
        related_posts = Post.objects.filter(categories__in=post_categories).distinct(
        ).annotate(similarity = Count("categories")).order_by("-date_created", "-similarity").exclude(pk=post.pk)
        last_related_posts = related_posts[0:5]
        related_categories = Category.objects.filter(posts__in=related_posts).exclude(sub_cat=None).distinct()
        share_url = request.build_absolute_uri(post.get_absolute_url())
    except Post.DoesNotExist:
        return render(request, "generals/404.html")
    return render(request, "blog/postd.html", context={"post": post, "share_url": share_url, "related_categories": related_categories, "related_posts": last_related_posts})


def post_filter_ajax(request):
    pid = request.GET.get("pid")
    base_cat_id = request.GET.get("base_cat_id")
    filtered_cat_ids = request.GET.get("cat_id")
    order_option = request.GET.get("order")
    success = True
    error = False
    posts = Post.acp_manage.all().annotate(views = Count("user_viewed")).order_by("-views", "-date_created")
    if pid:
        try:
            post = Post.objects.prefetch_related("categories").get(pk=pid)
            categories = post.categories.all()
            posts = posts.filter(categories__in=categories)
        except Post.DoesNotExist:
            error = True
            success = False
    if base_cat_id:
        try:
            category = Category.objects.prefetch_related(
                "posts").get(pk=base_cat_id)
            posts = posts.filter(categories__in=[category])
        except Category.DoesNotExist:
            error = True
            success = False
    if filtered_cat_ids:
        for cat_id in filtered_cat_ids.split(","):
            posts = posts.filter(categories__id__in=[cat_id])
    if order_option:
        if order_option == "newest":
            posts =  posts.order_by("-date_created")
        if order_option == "most_viewed":
            posts = posts.order_by("-views") 
    posts = posts.distinct()
    post_count = posts.count()
    paginator = Paginator(posts, 2)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(1)
    except PageNotAnInteger:
        posts = paginator.page(1)
    html = render_to_string(
        "post_partials/filtered_products_ajax.html", {"posts": posts})
    return JsonResponse({
        "html": html,
        "success": success,
        "error": error,
        "post_count": post_count,
    })
