from django.db import models
from django.urls import reverse


from django_jalali.db import models as Jmodels

from users.models import CostumUser


class PostACPManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="ACP")


class Category(models.Model):
    sub_cat = models.ForeignKey(
        "self", blank=True, null=True, verbose_name="بالا دسته", related_name="down_cats", on_delete=models.CASCADE)

    slug = models.SlugField(verbose_name="اسلاگ", allow_unicode=True)

    title = models.CharField(verbose_name="عنوان", max_length=100)
    des = models.TextField(verbose_name="توضیحات",
                           blank=True, null=True, max_length=100)

    avatar = models.ImageField(
        verbose_name="اواتار", blank=True, null=True, upload_to="category_images/")

    date_created = models.DateField(
        verbose_name="تاریخ ایجاد", auto_now_add=True)
    date_updated = models.DateField(
        verbose_name="اخرین بروزرسانی", auto_now=True)

    
    def get_absolute_url(self):
        return reverse("blog:category_detail", kwargs={"category_slug" : self.slug})
    
    
    def __str__(self):
        return f"{self.title}"
    
    
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        indexes = [
            models.Index(fields=["-date_created"])
        ]


class Post(models.Model):
    class Status(models.TextChoices):
        rejected = ("RJ", "ریجکت")
        draft = ("DRF", "نا معلوم")
        accepted = ("ACP", "تایید شده")
    slug = models.SlugField(verbose_name="اسلاگ",
                            help_text="بین کلمات - بگذارید", allow_unicode=True)

    categories = models.ManyToManyField(
        Category, verbose_name="دسته بندی",blank=True , null=True ,related_name="posts")

    title = models.CharField(verbose_name="عنوان", max_length=50)
    text = models.TextField(verbose_name="مقدمه",blank=True , null=True)

    date_created = Jmodels.jDateField(
        verbose_name="تاریخ انتشار", auto_now_add=True)
    date_updated = Jmodels.jDateField(
        verbose_name="اخرین بروزرسانی", auto_now=True)

    user_viewed = models.ManyToManyField(CostumUser, blank=True, null=True, related_name="viewed_posts", verbose_name="کاربران مشاهده کننده")
    
    objects = models.Manager()
    acp_manage = PostACPManager()

    author = models.ForeignKey(
        CostumUser, related_name="posts", verbose_name="نویسنده", on_delete=models.CASCADE)

    status = models.CharField(choices=Status.choices,
                              default=Status.draft, verbose_name="وضعیت", max_length=10)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_id" : self.pk, "post_slug" : self.slug})

    def __str__(self):
        return f"{self.author.get_fullname()}-{self.title}"

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست ها"
        ordering = ["-date_created",]
        indexes = [
            models.Index(fields=["-date_created"])
        ]


class Paragraph(models.Model):
    post = models.ForeignKey(to=Post, verbose_name="پست", help_text="این سایت از مارک دون پشتیبانی میکند",
                             on_delete=models.CASCADE, related_name="paragraphs")
    title = models.CharField(verbose_name="عنوان", max_length=100)
    text = models.TextField(verbose_name="متن", max_length=400)

    image = models.ImageField(verbose_name="تصویر(الزامی نیست)",
                              upload_to="posts/paraghraph_images/", blank=True, null=True)
    image_title = models.CharField(
        verbose_name="برای سئو عکس بهتر است وارد شود", blank=True, null=True, max_length=100)

    class Meta:
        verbose_name = "پراگراف"
        verbose_name_plural = "پراگراف ها"


    def delete(self, *args, **kwargs):
        path, storage = self.image.path, self.image.storage
        storage.delete(path)
        super().delete(*args, **kwargs)

    

    def __str__(self):
        return f"{self.post.title}-{self.title}"


class Comment(models.Model):
    class Status(models.TextChoices):
        rejected = ("RJ", "ریجکت")
        draft = ("DRF", "نا معلوم")
        accepted = ("ACP", "تایید شده")

    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE, verbose_name="پست")
    title = models.CharField(verbose_name="عنوان", max_length=50)
    text = models.TextField(verbose_name="متن", max_length=400)

    date_created = Jmodels.jDateField(
        verbose_name="تاریخ انتشار", auto_now_add=True)
    date_updated = Jmodels.jDateField(
        verbose_name="اخرین بروزرسانی", auto_now=True)

    status = models.CharField(choices=Status.choices,
                              default=Status.draft, verbose_name="وضعیت", max_length=100)

    def __str__(self):
        return f"{self.post.title}-{self.title}"

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"
        ordering = [
            "-date_created"
        ]


class PostFileManager(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="files", verbose_name="پست")
    title = models.CharField(verbose_name="عنوان", blank=True,
                             null=True, help_text="برای سئو بهتر است وارد شود", max_length=500)
    file = models.FileField(verbose_name="فایل(فیلم،عکس و ...)",
                            blank=True, null=True, upload_to="post_files/files/%Y/%m/%d/")
    image = models.ImageField(verbose_name="عکس", blank=True,
                              null=True, upload_to="post_files/images/%Y/%m/%d/")

    def delete(self, *args, **kwargs):
        path, storage = self.image.path, self.image.storage
        storage.delete(path)
        file_path, file_storage = self.file.path, self.file.storage
        file_storage.delete(file_path)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "فایل(وبلاگ)"
        verbose_name_plural = "فایل ها(وبلاگ)"
        
    def __str__(self):
        return f'{self.post.title}  {self.title}' 


