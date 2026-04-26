from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from django_jalali.db import models as jmodels


from users.models import CostumUser


# validators
def off_validator(value):
    if value > 100:
        raise ValidationError("تخفیف نمی تواند بیشتر از  صد در صد باشد")
    return value


class AmazingOfferMain(models.Model):
    products = models.ManyToManyField(
        "Product", verbose_name="محصولات", related_name="amazing_offer")
    off = models.PositiveSmallIntegerField(validators=[off_validator])
    datetime = models.DateTimeField(blank=True, null=True, verbose_name="مهلت")

    def __str__(self):
        return "پیشنهاد شگفت انگیز"

    class Meta:
        verbose_name = "پیشنهاد شگفت انگیز"
        verbose_name_plural = "پیشنهادات شگفت انگیز"


class Slider(models.Model):
    products = models.ManyToManyField(
        "Product", related_name="sliders", verbose_name="محصولات", blank=True, null=True)
    name = models.CharField(verbose_name="نام", max_length=50)
    image = models.ImageField(upload_to="slider/", verbose_name="تصویر")
    link = models.URLField(verbose_name="url مربوط به اسلاید",
                           help_text="درصورت وارد کردن این فیلد دیگر از فیلد محصولات استفاده نخواهد شد!", blank=True, null=True)

    date_created = jmodels.jDateField(
        auto_now_add=True, verbose_name="تاریخ ایجاد")
    date_updated = jmodels.jDateField(
        auto_now=True, verbose_name="اخرین بروزرسانی")

    def delete(self, *args, **kwargs):
        path, storage = self.image.path, self.image.storage
        storage.delete(path)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدر ها"
        ordering = [
            "-date_created"
        ]
        indexes = [
            models.Index(fields=["-date_created"])
        ]

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    sub_cat = models.ForeignKey("self", blank=True, null=True, related_name="down_cat",
                                verbose_name="دسته بندی بالا", on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="category_images/", blank=True, null=True, verbose_name="تصویر")

    CATBASE = (
        ("BR", "بر اساس برند"),
        ("CL", "بر اساس رنگ"),
    )
    cat_base = models.CharField(choices=CATBASE, blank=True, null=True, max_length=50)
    name = models.CharField(max_length=20, verbose_name="نام دسته بندی")
    slug = models.SlugField(verbose_name="اسلاگ")

    def get_absolute_url(self):
        return reverse("products:product_by_category", kwargs={"category_slug": self.slug})

    def delete(self, *args, **kwargs):
        storage, path = self.avatar.storage, self.avatar.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام رنگ")
    style_class = models.CharField(
        max_length=50, verbose_name="کلاس استایل در سی اس اس")

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ ها"
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی", related_name="products")

    today_delivery = models.BooleanField(default=False)
    seller_delivary = models.BooleanField(default=False)
    attendtent_sale = models.BooleanField(default=False)

    name = models.CharField(max_length=30, verbose_name="نام")
    slug = models.SlugField(verbose_name="اسلاگ")
    description = models.TextField(max_length=1000, verbose_name="توضیحات")

    price = models.PositiveIntegerField(
        verbose_name="قیمت")
    off = models.PositiveIntegerField(
        verbose_name="تخفیف", validators=[off_validator])
    price_after_off = models.PositiveIntegerField(
        verbose_name="قیمت پس از تخفیف", blank=True, null=True)
    inventory = models.PositiveIntegerField(verbose_name="موجودی")
    weight = models.PositiveIntegerField(verbose_name="وزن")

    colors = models.ManyToManyField(Color, blank=True, null=True, verbose_name="رنگ ها")
    has_colors = models.BooleanField(default=False, verbose_name="دارای رنگ بندی")



    favourite_by = models.ManyToManyField(
        CostumUser, related_name="favourite_products")

    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    colors_map= models.JSONField(verbose_name="مهم نیست:)", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.price_after_off = self.price * (1-(self.off / 100))

        super().save(*args, *kwargs)

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"product_id": self.pk, "product_slug": self.slug})

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["-date_created"])
        ]
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"






class ProductFileManager(models.Model):
    product = models.ForeignKey(
        Product, related_name="files", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="product_images/", verbose_name="تصویر")
    title = models.CharField(max_length=50, verbose_name="عنوان")

    def delete(self, *args, **kwargs):
        path, storage = self.image.path, self.image.storage
        storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "فایل "
        verbose_name_plural = "فایل ها"


class Feature(models.Model):
    product = models.ForeignKey(
        Product, related_name="features", on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name="نام")
    feature = models.CharField(max_length=40, verbose_name="ویژگی")

    class Meta:
        verbose_name = "ویژگی "
        verbose_name_plural = "ویژگی ها"

    def __str__(self):
        return f"{self.name}"


class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Comment.Status.PUBLISHED)


class UserOponionComment(models.Model):
    is_usefull = models.BooleanField(verbose_name="ایا کاربردی بود")
    user_from = models.ForeignKey(
        CostumUser, on_delete=models.CASCADE, verbose_name="کاربر", related_name="user_oponions")
    comment_to = models.ForeignKey(
        "Comment", verbose_name="کامنت", on_delete=models.CASCADE, related_name="user_oponions")

    class Meta:
        verbose_name = "نظر کاربر(کامنت)"
        verbose_name_plural = "نظرات کاربران(کامنت ها)"

    def __str__(self):
        return f'{"مفید بود" if self.is_usefull else "مفید نبود"}-{self.user_from.phone}-{self.comment_to.title}'


class Comment(models.Model):
    product = models.ForeignKey(
        Product, related_name="comments", on_delete=models.CASCADE)
    RATING = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    class Status(models.TextChoices):
        PUBLISHED = "PB", "published"
        DRAFT = "DR", "draft"
        REJECTED = "RJ", "rejected"

    user = models.ForeignKey(CostumUser, verbose_name="کاربر ارسال کننده",
                             on_delete=models.CASCADE, related_name="user_comments")
    status = models.CharField(choices=Status.choices, default=Status.DRAFT, max_length=3)

    users_oponion = models.ManyToManyField(
        CostumUser, related_name='comments', verbose_name="نظرات کاربران", blank=True, null=True, through=UserOponionComment)

    title = models.CharField(blank=True, null=True,
                             max_length=30, verbose_name="عنوان")
    text = models.TextField(verbose_name="نظر")
    rating = models.PositiveSmallIntegerField(
        choices=RATING, default=1, verbose_name="امتیاز")
    sugest_to_buy = models.BooleanField(
        blank=True, null=True, default=False, verbose_name="پیشنهاد خرید")

    date_created = jmodels.jDateTimeField(auto_now_add=True)
    date_updated = jmodels.jDateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.rating:
            self.rating = 5 if self.sugest_to_buy else 0
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["-date_created"])
        ]

    def __str__(self):
        return f"{self.title}-{self.product.name}"


# Create your models here.
