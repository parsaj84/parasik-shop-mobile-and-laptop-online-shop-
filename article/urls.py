from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("post-list/", view= views.posts_list, name="post_list"),
    path("post-list/<str:category_slug>/", view=views.posts_list, name="category_detail"),
    path("related-posts/<int:pid>/", view=views.posts_list, name="related_posts"),
    path("post-detail/<int:post_id>/<str:post_slug>/", view=views.article_detail, name="post_detail"),
    path("post-filter-ajax/", view=views.post_filter_ajax, name="post_filter_ajax"),
]