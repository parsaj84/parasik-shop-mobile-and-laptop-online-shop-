"""
URL configuration for parasik_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('parasik-shop-administration/', admin.site.urls),
    path("", include("products.urls", namespace="products")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("users/", include("users.urls", namespace="users") ),
    path("orders/", include("orders.urls", namespace="orders")),
    path("blog/", include("article.urls", namespace="blog")),
    path("API/", include("apis.urls", namespace="API")),
    
]

handler404 = "products.urls.handler404"

urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)

