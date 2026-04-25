from drf_spectacular.utils import inline_serializer, OpenApiResponse, OpenApiRequest, OpenApiParameter
from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.http import Http404

from products.models import Product, Category
from users.models import CostumUser
from orders.models import Order
from article.models import *


from .seializers import ProductSerializer, UserSerializer, PostHLModelSerilizer, CategorySerializer, OrderSerializer, PostSerializer


from rest_framework.settings import api_settings
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import views
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework import renderers
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import CursorPagination


from drf_spectacular.utils import extend_schema

from .permissions import CostumPerm, AnotherCostumPerm


class CostumAnonThrotlle(AnonRateThrottle):
    rate = "100/day"


# class MozPaginationClass(PageNumberPagination):
#     page_size = 1
#     page_query_param = "p"
#     page_size_query_param = "moz"
#     max_page_size = 3

class CustomCursorPagination(CursorPagination):
    ordering = "-date_created"
    page_size = 5


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = CustomCursorPagination


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        obj = super().get_object()
        print(obj)
        return obj


class UserListAPIView(views.APIView):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]

    def get(self, request, *args, **kwargs):
        users = CostumUser.objects.all()
        serializer = UserSerializer(users, many=True)

        if page := request.query_params.get("page"):
            paginator = PageNumberPagination()
            paginator.paginate_queryset()

        return Response(serializer.data)


class UserRegisterAPiView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serialized_recieved_data = UserSerializer(data=request.data)
        if not serialized_recieved_data.is_valid():
            return Response(serialized_recieved_data.errors)

        if CostumUser.objects.filter(phone=request.data.get("phone")).exists():
            return Response({"error": "phone is registered"})
        user = CostumUser(phone=request.data.get("phone"))
        user.set_password(request.data.get("password"))
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(request=OrderSerializer, responses=OrderSerializer)
class OrderView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailApiView(views.APIView):
    permission_classes = [CostumPerm]

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        order = Order.objects.get(pk=pk)
        serilaizer = OrderSerializer(order)
        print(request.user == order.seller)
        if not request.user == order.seller:
            return Response({"ridi": "ridi"})
        return Response(serilaizer.data)

    def get_object(self):
        obj = Order.objects.get(pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj


class PostApi(views.APIView):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    throttle_classes = [CostumAnonThrotlle]

    def get(self, request, *args, **kwargs):
        posts = Post.acp_manage.select_related(
            "author").prefetch_related("comments", "author", "categories")
        serializer = PostSerializer(posts, many=True)
        response = Response(serializer.data, headers={
                            "content_type": "application/json"})
        print(self.kwargs)
        return Response(serializer.data, headers={"content_type": "application/json"})
    #    return JsonResponse(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            try:
                print("mn")
                author = CostumUser.objects.get(
                    phone=serializer.validated_data.get("author", {}).get("id"))
                post = Post.objects.create(
                    author=author, title=serializer.validated_data["title"], text=serializer.validated_data["text"])
                for p in serializer.validated_data["paragraphs"]:
                    Paragraph.objects.create(post=post, **p)
                for c in serializer.validated_data["comments"]:
                    Comment.objects.create(post=post, **c)
                post.author = author
            except CostumUser.DoesNotExist:
                print("kj")
                author = CostumUser.objects.create(
                    **serializer.validated_data["author"])
                post = Post.objects.create(
                    author=author, title=serializer.validated_data["title"], text=serializer.validated_data["text"])
                for p in serializer.validated_data["paragraphs"]:
                    Paragraph.objects.create(post=post, **p)
                for c in serializer.validated_data["comments"]:
                    Comment.objects.create(post=post, **c)
                post.author = author
            post.save()
            return Response({"staus": "done"})
        else:
            return Response(serializer.errors)

    def delete(self, request):
        post_id = request.query_params.get("post_id")
        print(post_id)
        Post.objects.filter(id=post_id).delete()
        return Response({"response": "post deleted successfully"})


class PostUpdateView(views.APIView):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]
    renderer_classes = [renderers.StaticHTMLRenderer]

    def put(self, request, pk):
        data = request.data
        try:
            post = Post.objects.get(pk=pk)
            for category in data.get("categories"):
                try:
                    category = Category.objects.get(slug=data.get("slug"))
                    for key, value in category.items():
                        setattr(category, key, value)
                        category.save()
                except Category.DoesNotExist:
                    category = Category.objects.create(**category)
                    post.categories.add(category)
            for paragraph_dict in data.get("paragraphs"):
                try:
                    paragraph = Paragraph.objects.get(
                        pk=paragraph_dict.get("pk"))
                    for key, value in paragraph_dict:
                        if key != "image":
                            setattr(paragraph, key, value)
                        paragraph.save()
                except Paragraph.DoesNotExist:
                    paragraph = Paragraph.objects.create(
                        post=post, **paragraph_dict)
            try:
                author = CostumUser.objects.get(
                    phone=data.get("author").get("phone"))
            except CostumUser.DoesNotExist:
                return Response("<html></html>")

            data.pop("comments")
            data.pop("author")
            data.pop("paragraphs")
            data.pop("categories")
            data.pop("id")
            for key, value in data.items():
                setattr(post, key, value)
            post.save()
            serialzer = PostSerializer(post)
            return Response(serialzer.data)
        except Post.DoesNotExist:
            html = render_to_string(template_name="products/productl.html")
            return Response(html)


class PostDestroyAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


@api_view(http_method_names=["post", "get"])
@authentication_classes(authentication_classes=[BasicAuthentication])
@permission_classes(permission_classes=[AllowAny])
def post_list_api(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    print(serializer.instance)
    return Response(serializer.data)


class TestHTMLRender(views.APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = "api/test.html"
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return HttpResponse("404")
        serialzer = PostSerializer(post)
        return Response({"serializer": serialzer, "post": post})

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Http404()
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            message = "post updated successfully"
        else:
            post = None
            message = "data is not valid"
        return Response({"serializer": serializer, "post": post, "message": message})


@api_view(["GET"])
@permission_classes([AllowAny])
def test(request):
    request.body.decode("utf-8")
    print(request.data)
    return Response({"moz": "moz"})


class ProductRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_url_kwarg = "moz"
    lookup_field = "id"
    queryset = Product.objects.all()
    permission_classes = [AnotherCostumPerm]


class SpectacularExampleAPIView(views.APIView):
    permission_classes = [AllowAny]

    @extend_schema(parameters=[OpenApiParameter(name="moz", description="پارامتر برای فهم موز بودن یا نبودن!", type=OpenApiTypes.STR, location="query", )], responses={200: inline_serializer(name="moz", fields={"moz": serializers.CharField(), "serialize_moz": ProductSerializer()}), 403: OpenApiResponse(description="moz bazi dar avordi calack", response=inline_serializer(name="moz", fields={"moz_field": serializers.CharField()}))}, tags=["Moz"])
    def get(self, request):
        print(request.META.get("HTTP_ADDRESS", "no address"))
        return Response({"moz": "moz"})
