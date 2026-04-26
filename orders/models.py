from django.db import models
from django.core import validators
from django.utils import timezone


from django_jalali.db import models as jmodels
import pytz
from django_jalali.templatetags import jformat


from datetime import timedelta

from products.models import Product, Color
from users.models import CostumUser, Address


class Order(models.Model):
    buyer = models.ForeignKey(
        CostumUser, related_name="orders", on_delete=models.CASCADE, verbose_name="خریدار")
    seller = models.ForeignKey(CostumUser, related_name="selling_orders",
                               blank=True, null=True, verbose_name="فروشنده", on_delete=models.CASCADE)
    address = models.ForeignKey(
        to=Address, verbose_name="ادرس", related_name="orders", on_delete=models.CASCADE)
    fname = models.CharField(max_length=20, verbose_name="نام")
    lname = models.CharField(max_length=20, verbose_name="نام خانوادگی")
    phone = models.CharField(max_length=11, verbose_name="شماره تلفن", validators=[validators.RegexValidator(regex=r'^(\+98|0)?9\d{9}$',
                                                                                                             code="invalid_phone",
                                                                                                             message="invalid phone")], error_messages={"invalid_phone": "این شماره تلفن معتبر نیست"})
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی", validators=[validators.RegexValidator(
        regex=r'^\d{10}$', code="postall_code")], error_messages={"postall_code": "کد پستی نامعتبر"})
    des = models.CharField(max_length=100, blank=True,
                           null=True, verbose_name="توضیحات")

    date_created = jmodels.jDateTimeField(
        auto_now_add=True, verbose_name="تاریخ سفارش")
    date_updated = jmodels.jDateTimeField(
        auto_now=True, verbose_name="اخرین بروزرسانی")
    date_delivery = jmodels.jDateField(
        verbose_name="زمان تقریبی ارسال", blank=True, null=True)

    date_given_to_post = jmodels.jDateField(
        verbose_name="تاریخ تحویل به پست", blank=True, null=True)

    is_rejected = models.BooleanField(default=False, verbose_name="مرجوعی")
    is_paid = models.BooleanField(verbose_name="پرداخت شده", default=False)

    POST_CHOICES = (
        ("PSH", "پیشتاز"),
        ("MN", "معمولی")
    )

    ORDER_STATUS = (
        ("PRC", "در حال پردازش"),
        ("DELIVERY", "تحویل به پست"),
    )

    status = models.CharField(choices=ORDER_STATUS, blank=True, null=True, max_length=100)

    send_price = models.PositiveBigIntegerField(
        verbose_name="هزینه ارسال", blank=True, null=True)

    post_type = models.CharField(
        choices=POST_CHOICES, default="MN", verbose_name="نوع پست",max_length=100)
    total_price = models.PositiveBigIntegerField(
        blank=True, null=True, verbose_name="قیمت کل سفارش", max_length=100)

    tracking_id = models.CharField(verbose_name= "شماره پیگیری" ,blank=True, null=True, max_length=8, unique=True, error_messages={"unique" : "مقدار شماره پیگیری باید یکتا باشد"})

    def save(self, *args, **kwargs):
        previous = self.__class__.objects.filter(pk=self.pk)
        new_obj = self
        saved_from_fake_payment =False
        if kwargs.get("saved_from_fake_payment"):
            saved_from_fake_payment = kwargs.pop("saved_from_fake_payment")
        if saved_from_fake_payment:
            if not previous.first().is_paid and self.is_paid:
                Notfication.objects.create(user=self.buyer, order=self, title="ثبت سفارش",
                        text=f" سفارش شما با شماره{self.tracking_id} ثبت شده. ", type="ORD")   
        else:
            if previous.exists():
                if not previous.first().is_paid and self.is_paid:
                    Notfication.objects.create(user=self.buyer, order=self, title="ثبت سفارش",
                                            text=f"سفارش شما با {self.tracking_id} ثبت در حال پردازش است. ", type="ORD")
                    self.status = "PRC"
                else:
                    new_obj = self
                    if previous.first().status != new_obj.status:
                        Notfication.objects.create(user=self.buyer, order=new_obj, title="وضعیت سفارش",
                                                text=f"سفارش شما با سفارش {self.tracking_id} در مرحله {new_obj.get_status_str()}  قرار دارد.", type="ORD")
                        if new_obj.is_paid and new_obj.status == "DELIVERY":
                            self.date_given_to_post = timezone.now().astimezone(pytz.timezone("Asia/Tehran"))
                if self.status == "DELIVERY" and self.status != previous.first().status:
                    self.date_given_to_post = timezone.now().astimezone(pytz.timezone("Asia/Tehran"))
            if self.is_paid and not self.date_delivery:
                now_tehran = timezone.now().astimezone(pytz.timezone("Asia/Tehran")).date()
                duration_days = 3 if self.buyer.province == "thr" else 5
                self.date_delivery = now_tehran + timedelta(days=duration_days)
        
        super().save(*args, **kwargs)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_status_str(self):
        for status in self.ORDER_STATUS:
            if status[0] == self.status:
                return status[1]
        return "نامعلوم"

    def __str__(self):
        return f"{self.buyer.get_fullname()}-{self.buyer.phone}-{self.date_created}"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["-date_created"])
        ]


class Item(models.Model):
    order = models.ForeignKey(
        Order, verbose_name="سفارش", related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, verbose_name="محصول", related_name="in_orders", on_delete=models.CASCADE)

    price = models.PositiveBigIntegerField(verbose_name="قیمت")
    weight = models.PositiveIntegerField(verbose_name="وزن")
    quantity = models.PositiveIntegerField(verbose_name="تعداد")
    color = models.JSONField(verbose_name="color map", blank=True, null=True)


    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ایتم"

    class Meta:
        verbose_name = "ایتم"
        verbose_name_plural = "ایتم ها"


class Transcation(models.Model):
    reciever = models.ForeignKey(
        CostumUser, related_name="revieved_transcations", verbose_name="گیرنده", on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey(CostumUser, verbose_name="فرستنده",
                               related_name="sent_transcations", on_delete=models.CASCADE, blank=True, null=True)
    date_teked_place = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ واریز")
    price = models.PositiveBigIntegerField(verbose_name="مبلغ")
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, verbose_name="تراکنش مربوط", related_name="transaction")

    date_created = jmodels.jDateField(auto_now_add=True)
    date_updated = jmodels.jDateField(auto_now=True)

    def __str__(self):
        return f"تراکنش کاربر {self.sender.phone} برای سفارش {self.order}"

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنشات"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["-date_created"])
        ]


class OffCode(models.Model):
    orders = models.ManyToManyField(
        Order, blank=True, null=True, related_name="off_codes")
    users = models.ManyToManyField(
        CostumUser, related_name="off_codes", verbose_name="کاربران")
    code = models.CharField(unique=True, error_messages={
                            "unique": "این کد تخفیف قیلا ثبت شده است"}, verbose_name="کد تخفیف", max_length=30)
    min_price = models.PositiveBigIntegerField(verbose_name="کف خرید")
    OFF_TYPE = (
        ("FRSE", "ارسال رایگان"),
        ("PRDC", "کاهش قیمت")
    )

    off_type = models.CharField(
        choices=OFF_TYPE, default="FRSE", verbose_name="نوع تخفیف", max_length=100) 
    price_decreament = models.PositiveBigIntegerField(
        verbose_name="کاهش قیمت", help_text="فقط در صورتی تعیین شود که نوع کو کاهش قیمت است.")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کد های تخفیف"


class Notfication(models.Model):
    user = models.ForeignKey(CostumUser, related_name="notifications",
                             on_delete=models.CASCADE, verbose_name="کاربر")
    title = models.CharField(max_length=50, verbose_name="عنوان",)
    text = models.TextField(max_length=300, verbose_name="متن پیام")
    date_created = jmodels.jDateTimeField(auto_now_add=True)

    order = models.ForeignKey(Order, verbose_name="سفارش", help_text="در صورتی که نوع پیام مرحله سفارش باشد باید وارد شود!",
                              blank=True, null=True, on_delete=models.CASCADE, related_name="notifiations")
    offcode = models.ForeignKey(OffCode, verbose_name="کد تخفیف", related_name="nitifications", blank=True,
                                null=True, on_delete=models.CASCADE, help_text="درصورتی نوع پیام کد تخفیف باشد باید واردش شود")

    NOTIFICATION_TYPE = (
        ("ORD", "مرحله سفارش"),
        ("OFC", "کد تخفیف"),
        ("OTH", "متفرقه")
    )

    type = models.CharField(choices=NOTIFICATION_TYPE, verbose_name="نوع پیام", max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["-date_created"])
        ]


class RefrallRequest(models.Model):
    user = models.ForeignKey(CostumUser, related_name="refrall_reqeusts",
                             on_delete=models.CASCADE, verbose_name="کاربر ثبت گننده")
    item = models.OneToOneField(Item, related_name="refrall_request",
                                verbose_name="ایتم مربوطه", on_delete=models.CASCADE)
    reason = models.TextField(max_length=100, verbose_name="دلیل")
    image = models.ImageField(
        verbose_name="تصویر", upload_to="refrall_requests/", blank=True, null=True)

    is_accepted = models.BooleanField(default=False, verbose_name="قبول شده!")

    date_created = jmodels.jDateField(
        auto_now_add=True, verbose_name="تاریخ ایجاد")
    date_updated = jmodels.jDateField(
        auto_now=True, verbose_name="اخرین بروزرسانی")

    def save(self, *args, **kwargs):
        previous = self.__class__.objects.filter(pk=self.pk)
        new = self
        if previous.exists():
            if previous[0].is_accepted != new.is_accepted and new.is_accepted:
                Notfication.objects.create(user=self.user, title="قبول شدن درخواست مرجوعی",
                                           text=f"درخواست مرجوعی شما برروی ایتیم {self.item.product.name} قبول وهزینه مربوط به ان به شما پرداخت خواهد شد.", type="OTH")
        else:
            if new.is_accepted:
                Notfication.objects.create(user=self.user, title="قبول شدن درخواست مرجوعی",
                                           text=f"درخواست مرجوعی شما برروی ایتیم {self.item.product.name} قبول وهزینه مربوط به ان به شما پرداخت خواهد شد.", type="OTH")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        path, storage = self.image.path, self.image.storage
        storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"درخواست مرجوعی {self.item.product.name} کاربر {self.user.phone}"

    class Meta:
        verbose_name = "درخواست مرجوعی"
        verbose_name_plural = "درخواست های مرجوعی"
        indexes = [
            models.Index(fields=["-date_created"])

        ]
        ordering = [
            "-date_created"
        ]
