from django import forms
from django.core.exceptions import ValidationError


from .models import CostumUser


import re

def regex_validator(regix , string):
    return re.fullmatch(pattern=regix, string=string)

class UserAdminCreateForm(forms.ModelForm):
    class Meta:
        model = CostumUser
        fields = ["phone", "password", "first_name", "last_name", "email", "national_code",
                  "province", "city", "avatar", "is_seller", "is_active", "is_superuser", "is_staff"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user




class UserUpdateAccount(forms.ModelForm):
    class Meta:
        model = CostumUser
        fields = [ "first_name", "last_name", "email",
                  "birthday", "national_code"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder" : "نام","class": """block w-full p-2.5 text-base outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400 transition-all
                      text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400"""}),
            "last_name": forms.TextInput(attrs={"placeholder" : "نام خانوادگی","class": """block w-full p-2.5 text-base outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400 transition-all
                      text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400"""}),
            "email": forms.TextInput(attrs={"placeholder" : "ایمیل","class": """block w-full p-2.5 text-base outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400 transition-all
                      text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400"""}),
            "birthday": forms.TextInput(attrs={"placeholder" : "تاریخ تولد","placeholder" : "مثال : 1380/04/04","class": """block w-full p-2.5 text-base outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400 transition-all
                      text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400"""}),
            "national_code" : forms.TextInput(attrs={"placeholder" : "کد ملی","class" : """block w-full p-2.5 text-base outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400 transition-all
                      text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400""", "oninput" : "this.value = this.value.replace(/[^0-9]/g, '')"}),
        }

        labels  = {
            "phone" : "شماره تلفن",
            "first_name" : "نام",
            "last_name" : "نام خانوادگی",
            "national_code" : "کد ملی",
            "birthday": "تاریخ تولد",

            "email" : " ایمیل"
            
        }
    def clean_email(self):
        email = self.cleaned_data["email"]
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not regex_validator(regix=pattern, string=email):
            raise ValidationError("ایمیل نامعتبر")
        if email:
            if CostumUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                raise ValidationError("این ایمیل قبلا ثبت شده است")                                                        
        return email
    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if phone:
            if CostumUser.objects.exclude(pk=self.instance.pk).filter(phone = phone).exists():
                raise ValidationError("این شماره موبایل قبلا ثبت شده است!")
        return phone
    
    # def clean_birthday(self):
    #     # birthday = self.cleaned_data["birthday"]
    #     # pattern = r'^(1[3-9]\d{2}|[2-9]\d{3})/(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])$'
    #     # if birthday:
    #     #     if not regex_validator(regix=pattern, string=str(birthday)):
    #     #         raise ValidationError("لطفا تاریخ را با فرمت مناسب وارد کنید!")    
    #     # birthday_units = birthday.split("/")
    #     # return "-".join(birthday_units)
    
    def clean_national_code(self):
        national_code = self.cleaned_data["national_code"]
        if national_code:
            if not regex_validator(regix= r"^\d{10}$", string=national_code):
                raise ValidationError("لطفا یک کدملی معتبر وارد کنید!")
        return national_code