from django.urls import path, include

from rest_framework.routers import DefaultRouter

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from . import views

app_name = "API"

router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet)

urlpatterns = [
    path("product-list/", view=views.ProductListAPIView.as_view()),
    path("product-detail/<int:pk>/", views.ProductDetailView.as_view()),
    path("users/", view=views.UserListAPIView.as_view(), name="user_api"),
    path("user-register/", view=views.UserRegisterAPiView.as_view(),
         name="register_user_api"),
    path("orders/", views.OrderView.as_view()),
    path("orders/<int:pk>", views.OrderDetailApiView.as_view()),
    path("post-list-api/", view=views.PostApi.as_view()),
    path("fbv-post-api/", views.post_list_api),
    path("", include(router.urls)),
    path("post-delete/<int:pk>/", views.PostDestroyAPIView.as_view()),
    path("post-update-api/<int:pk>/", views.PostUpdateView.as_view()),
    path("post-update-html/<int:pk>/", view=views.TestHTMLRender.as_view()),
    path("test/", view=views.test),
    path("test-swagger/", view=views.SpectacularExampleAPIView.as_view(), name="spectacular test"),
    path("test-generic/<int:moz>/", view=views.ProductRetriveAPIView.as_view()),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='API:schema'), name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='API:schema'), name='redoc'),
]
