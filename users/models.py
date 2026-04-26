from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators





from django_jalali.db import models as jmodels


class PhoneExist(Exception):
    pass


class EmailExist(Exception):
    pass


class CostumUserManager(UserManager):
    def create_user(self, phone=None, password=None, first_name=None, last_name=None, email=None, national_code=None, avatar=None, is_seller=False, is_active=True, is_superuser=False, is_admin=False, is_staff=False):
        if phone:
            if self.get_queryset().filter(phone=phone).exists():
                raise PhoneExist()
        if email:
            if self.get_queryset().filter(email=email).exists():
                raise EmailExist()
            email = self.normalize_email(email=email)
        user = self.model(phone=phone,
                          first_name=first_name,
                          last_name=last_name,
                          email=email,
                          national_code=national_code,
                          avatar=avatar,
                          is_seller=is_seller,
                          is_active=is_active,
                          is_staff=is_staff,
                          is_admin=is_admin,
                          is_superuser = is_superuser,
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone,password, email=None, is_active=True, is_admin=True, is_seller=True, is_staff=True):
        self.create_user(phone=phone, password=password, email=email, is_active=is_active,
                         is_admin=is_admin, is_seller=is_seller, is_staff=is_staff)
        


class CostumUser(AbstractBaseUser, PermissionsMixin):
    PROVINCE_CHOICES = (
        ('thr', 'تهران'),
        ('khr', 'خراسان رضوی'),
        ('esf', 'اصفهان'),
        ('azb', 'آذربایجان شرقی'),
        ('frs', 'فارس'),
        ('kuz', 'خوزستان'),
        ('qom', 'قم'),
        ('krm', 'کرمانشاه'),
        ('azw', 'آذربایجان غربی'),
        ('gil', 'گیلان'),
        ('sbn', 'سیستان و بلوچستان'),
        ('ham', 'همدان'),
        ('krn', 'کرمان'),
        ('yzd', 'یزد'),
        ('ard', 'اردبیل'),
        ('hrm', 'هرمزگان'),
        ('mrk', 'مرکزی'),
        ('gol', 'گلستان'),
        ('mzn', 'مازندران'),
        ('smn', 'سمنان'),
        ('skh', 'خراسان جنوبی'),
        ('lrs', 'لرستان'),
        ('znj', 'زنجان'),
        ('krd', 'کردستان'),
        ('qaz', 'قزوین'),
        ('koh', 'کهگیلویه و بویراحمد'),
        ('nkh', 'خراسان شمالی'),
        ('ilam', 'ایلام'),
        ('chb', 'چهارمحال و بختیاری'),
        ('alb', 'البرز'),
        ('gms', 'قمصر'),  # (اختیاری، در صورت نیاز)
    )

    CITY_CHOICES = (
        ('thr-tehran', 'تهران'),
        ('khr-mashhad', 'مشهد'),
        ('esf-isfahan', 'اصفهان'),
        ('azb-tabriz', 'تبریز'),
        ('frs-shiraz', 'شیراز'),
        ('kuz-ahvaz', 'اهواز'),
        ('qom-qom', 'قم'),
        ('krm-kermanshah', 'کرمانشاه'),
        ('azb-urmia', 'ارومیه'),
        ('gil-rasht', 'رشت'),
        ('sbn-zahedan', 'زاهدان'),
        ('ham-hamedan', 'همدان'),
        ('krm-kerman', 'کرمان'),
        ('yzd-yazd', 'یزد'),
        ('ard-ardabil', 'اردبیل'),
        ('hrm-bandarabbas', 'بندرعباس'),
        ('mrk-arak', 'اراک'),
        ('thr-eslamshahr', 'اسلامشهر'),
        ('znj-zanjan', 'زنجان'),
        ('krd-sanandaj', 'سنندج'),
        ('qaz-qazvin', 'قزوین'),
        ('lrs-khorramabad', 'خرم‌آباد'),
        ('gol-gorgan', 'گرگان'),
        ('mzn-sari', 'ساری'),
        ('smn-shahroud', 'شاهرود'),
        ('skh-birjand', 'بیرجند'),
        ('kuz-abadan', 'آبادان'),
        ('kuz-dezfoul', 'دزفول'),
        ('esf-kashan', 'کاشان'),
        ('nkh-bojnourd', 'بجنورد'),
        ('smn-semnan', 'سمنان'),
        ('thr-fardis', 'فردیس'),
        ('koh-yasuj', 'یاسوج'),
        ('azb-khoy', 'خوی'),
        ('azb-maragheh', 'مراغه'),
        ('thr-qods', 'قدس'),
        ('mrk-saveh', 'ساوه'),
        ('thr-malard', 'ملارد'),
        ('mzn-babol', 'بابل'),
        ('mzn-nakhab', 'نکا'),
        ('krn-kerman', 'کرمان'),
        ('krn-baft', 'بافت'),
        ('krn-jiroft', 'جیرفت'),

    )
    
    phone = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن", validators=[validators.RegexValidator(
        regex=r'^(\+98|0)?9\d{9}$',
        message='Enter a valid Iranian phone number.',
        code='invalid_iranian_phone'
    )], error_messages={"invalid_iranian_phone": "شماره تلفن نامعتبر", "unique": "شماره تلفن قبلا وارد شده"})
    first_name = models.CharField(
        max_length=30, verbose_name="نام", blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    national_code = models.CharField(
    verbose_name="کد ملی", blank=True, null=True, max_length = 10, validators=[validators.RegexValidator(regex= r"^\d{10}$", code="invalid_national_code")], error_messages={"invalid_national_code" : "لطفا کدملی معتبر وارد کنید"})

    city = models.CharField(choices=CITY_CHOICES,
                            verbose_name="شهر", blank=True, null=True, max_length=50)
    province = models.CharField(
        choices=PROVINCE_CHOICES, verbose_name="استان", blank=True, null=True, max_length=50)

    wallet = models.PositiveIntegerField(
        blank=True, null=True, default=0, verbose_name="کیف پول")

    avatar = models.ImageField(
        verbose_name="اواتار", upload_to="users_avatar/")

    user_manager = CostumUserManager()
    objects = UserManager()

    birthday = jmodels.jDateField(
        blank=True, null=True, verbose_name="تاریخ تولد")
    date_joined = models.DateField(blank=True, null=True, auto_now_add=True)

    is_seller = models.BooleanField(verbose_name="فروشنده", default=False)
    is_active = models.BooleanField(verbose_name="فعال", default=True)
    is_superuser = models.BooleanField(verbose_name="super", default=False)
    is_admin = models.BooleanField(verbose_name="ادمین", default=False)
    is_staff = models.BooleanField(verbose_name="کارمند", default=False)

    USERNAME_FIELD = "phone"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_fullname(self):
        name  = f'{self.first_name} {self.last_name}' if self.first_name and self.last_name else None
        return name

    def delete(self, *args, **kwargs):
        if self.avatar:
            path ,storage = self.avatar.path , self.avatar.storage
            storage.delete(path)
        super().delete(*args, **kwargs)


    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-date_joined"]
        indexes = [models.Index(fields=["-date_joined"])]
    
    def __str__(self):
        return f"{self.get_fullname()}-{self.phone}"



class Address(models.Model):
    user = models.ForeignKey(CostumUser, verbose_name="ادرس ها",
                             related_name="addresses", on_delete=models.CASCADE)
    PROVINCE_CHOICES = (
        ('thr', 'تهران'),
        ('khr', 'خراسان رضوی'),
        ('esf', 'اصفهان'),
        ('azb', 'آذربایجان شرقی'),
        ('frs', 'فارس'),
        ('kuz', 'خوزستان'),
        ('qom', 'قم'),
        ('krm', 'کرمانشاه'),
        ('azw', 'آذربایجان غربی'),
        ('gil', 'گیلان'),
        ('sbn', 'سیستان و بلوچستان'),
        ('ham', 'همدان'),
        ('krn', 'کرمان'),
        ('yzd', 'یزد'),
        ('ard', 'اردبیل'),
        ('hrm', 'هرمزگان'),
        ('mrk', 'مرکزی'),
        ('gol', 'گلستان'),
        ('mzn', 'مازندران'),
        ('smn', 'سمنان'),
        ('skh', 'خراسان جنوبی'),
        ('lrs', 'لرستان'),
        ('znj', 'زنجان'),
        ('krd', 'کردستان'),
        ('qaz', 'قزوین'),
        ('koh', 'کهگیلویه و بویراحمد'),
        ('nkh', 'خراسان شمالی'),
        ('ilam', 'ایلام'),
        ('chb', 'چهارمحال و بختیاری'),
        ('alb', 'البرز'),
        ('gms', 'قمصر'),  # (اختیاری، در صورت نیاز)
    )

    CITY_CHOICES = (
        ('thr-tehran', 'تهران'),
        ('khr-mashhad', 'مشهد'),
        ('esf-isfahan', 'اصفهان'),
        ('azb-tabriz', 'تبریز'),
        ('frs-shiraz', 'شیراز'),
        ('kuz-ahvaz', 'اهواز'),
        ('qom-qom', 'قم'),
        ('krm-kermanshah', 'کرمانشاه'),
        ('azb-urmia', 'ارومیه'),
        ('gil-rasht', 'رشت'),
        ('sbn-zahedan', 'زاهدان'),
        ('ham-hamedan', 'همدان'),
        ('krm-kerman', 'کرمان'),
        ('yzd-yazd', 'یزد'),
        ('ard-ardabil', 'اردبیل'),
        ('hrm-bandarabbas', 'بندرعباس'),
        ('mrk-arak', 'اراک'),
        ('thr-eslamshahr', 'اسلامشهر'),
        ('znj-zanjan', 'زنجان'),
        ('krd-sanandaj', 'سنندج'),
        ('qaz-qazvin', 'قزوین'),
        ('lrs-khorramabad', 'خرم‌آباد'),
        ('gol-gorgan', 'گرگان'),
        ('mzn-sari', 'ساری'),
        ('smn-shahroud', 'شاهرود'),
        ('skh-birjand', 'بیرجند'),
        ('kuz-abadan', 'آبادان'),
        ('kuz-dezfoul', 'دزفول'),
        ('esf-kashan', 'کاشان'),
        ('nkh-bojnourd', 'بجنورد'),
        ('smn-semnan', 'سمنان'),
        ('thr-fardis', 'فردیس'),
        ('koh-yasuj', 'یاسوج'),
        ('azb-khoy', 'خوی'),
        ('azb-maragheh', 'مراغه'),
        ('thr-qods', 'قدس'),
        ('mrk-saveh', 'ساوه'),
        ('thr-malard', 'ملارد'),
        ('mzn-babol', 'بابل'),
        ('mzn-nakhab', 'نکا'),
    )

    name = models.CharField(max_length=20, verbose_name="نام ادرس")
    province = models.CharField(choices=PROVINCE_CHOICES, verbose_name="استان", max_length=50)
    city = models.CharField(choices=CITY_CHOICES,
                            max_length=20, verbose_name="شهر")
    reciever = models.CharField(max_length=100, verbose_name="تحویل گیرنده")
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی")
    phone = models.CharField(max_length=11, verbose_name="شماره تلفن گیرنده")
    address = models.TextField(verbose_name="ادرس")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ادرس'
        verbose_name_plural = 'ادرس ها'





# Create your models here.
