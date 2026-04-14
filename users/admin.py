from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from django_jalali.admin.filters import JDateFieldListFilter

from .forms import UserAdminCreateForm
from orders.models import CostumUser, Address,Notfication


class AddressInLine(admin.TabularInline):
    model = Address
    fields = ["name", "address", "postal_code"]
    extra = 0

class NotificationInline(admin.TabularInline):
    model = Notfication
    fields = ["title", "text", "type"]
    extra = 0

class CostumUserAdmin(UserAdmin):
    
    model = CostumUser
    list_filter = [("birthday", JDateFieldListFilter),]
    fieldsets = (("اطلاعات اصلی", {"fields": ["phone", "email", "password"]}),
                 ("اطلاعات کلی", {"fields": [
                  "first_name", "last_name", "wallet", "national_code", "avatar"]}),
                 ("تاریخ های مهم", {"fields": ["birthday","last_login"]}),
                 ("دسترسی ها", {"fields": [
                  "is_admin", "is_active", "is_staff", "is_superuser", "user_permissions"]}),
                 ("مکان", {"fields": ["province", "city"]})
                 )
    list_display = ["phone", "email", "first_name", "last_name", "date_joined"]
    inlines = [AddressInLine, NotificationInline]
    search_fields = ["phone","@first_name"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "usable_password", "password1", "password2"),
            },
        ),
    )


admin.site.unregister(Group)
admin.site.register(CostumUser, CostumUserAdmin)

# Register your models here.
