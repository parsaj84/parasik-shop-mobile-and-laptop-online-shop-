from rest_framework import serializers
from rest_framework.parsers import BaseParser
from rest_framework import validators

serializers.ListSerializer

from products.models import Product, ProductFileManager, Category
from users.models import CostumUser, Address
from orders.models import Order, Item
from article.models import Post, Comment, Category, Paragraph


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFileManager
        fields = ["image", "title"]

class DynamicFieldsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)
    
        if fields:
            allowed_fields = set(fields)
            existing_fileds = set(self.fields)

            for field in existing_fileds - allowed_fields:
                self.fields.pop(field)
    


class ProductSerializer(DynamicFieldsSerializer):

    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["name", "price", "price_after_off", "price", "off", "files"]


class AdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["name", "reciever", "province", "city"]


class UserSerializer(serializers.ModelSerializer):
    addresses = AdressSerializer(many=True, read_only=True)
    class Meta:
        model = CostumUser
        fields = ["id", "phone", "first_name", "last_name", "addresses"]


    def validate_first_name(self, value):
        if value == "parsa":
            raise serializers.ValidationError("parsa cant be valid")
        return value


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ["name", "slug", "products"]


class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Item
        fields = ["price", "weight", "quantity", "price", "product"]


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ["fname", "lname",
                  "phone", "postal_code", "des",
                  "date_created", "date_updated", "is_rejected", "is_paid", "post_type", "items"]


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["slug", "title", "des", "avatar",
                  "date_created", "date_updated"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["title", "text", "date_created", "date_updated", "status"]


class ParagraphSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ["id", "title", "text"]


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    categories = PostCategorySerializer(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    paragraphs = ParagraphSerilaizer(many=True)

    class Meta:
        model = Post
        fields = ["id", "title", "text", "date_created", "date_updated",
                  "author", "categories", "comments", "paragraphs"]

    def build_standard_field(self, field_name, model_field):
        return super().build_standard_field(field_name, model_field)

    def update(self, instance, validated_data):
        author = CostumUser.objects.get(
            phone=validated_data.get("author", {}).get("phone"))
        for category_dict in validated_data.get("categories"):
            try:
                category = Category.objects.get(
                    slug=validated_data.get("slug"))
            except Category.DoesNotExist:
                category = Category.objects.create(**category_dict)
            for key, value in category_dict.items:
                setattr(category, key, value)
            category.save()
        for paragraph in validated_data.get("paragraphs"):
            try:
                paragraph = Paragraph.objects.get(pk=paragraph.get("pk"))
                for key, value in paragraph.items:
                    setattr(paragraph, key, value)
                paragraph.save()
            except Paragraph.DoesNotExist:
                paragraph = Paragraph.objects.create(**paragraph)
        validated_data.pop("author")
        validated_data.pop("categories")
        validated_data.pop("comments")
        validated_data.pop("paragraphs")
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class ParagraphCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ["title", "text"]

    def create(self, validated_data):
        paragraph = Paragraph.objects.create(**validated_data)
        return paragraph


class PostCreateSerializer(serializers.ModelSerializer):
    paragraphs = ParagraphSerilaizer(many=True)
    class Meta:
        model = Post
        fields = ["title", "text", "paragraphs"]

    def create(self, validated_data):
        post = Post.objects.create(title=validated_data.get(
            "title"), text=validated_data.get("text"))
        return post


class PostHLModelSerilizer(serializers.HyperlinkedModelSerializer):
    paragraphs = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="blog:p_detail",  
        lookup_field="pk"
    )

    class Meta:
        model = Post
        fields = ["title", "paragraphs"]


