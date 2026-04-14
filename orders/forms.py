from django import forms

from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["fname", "lname","phone","postal_code","des"]
        widgets = {
            "fname" : forms.TextInput(attrs={"placeholder" : "نام*", "class" : """block w-full py-1.5 px-3 text-base outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400   transition-all col-span-6
                            text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400 h-11""", }),
            "lname" : forms.TextInput(attrs={"placeholder" : "نام خانوادگی*", "class" : """block w-full py-1.5 px-3 text-base outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400   transition-all col-span-6
                            text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400 h-11""", }),
            "phone" : forms.TextInput(attrs={"placeholder" : "تلفن همراه*", "class" : """block w-full py-1.5 px-3 text-base outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400   transition-all col-span-6
                            text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400 h-11""", "oninput" : "this.value = this.value.replace(/[^0-9]/g, '')"}),
            "postal_code" : forms.TextInput(attrs={"placeholder" : "کد پستی*", "class" : """block w-full py-1.5 px-3 text-base outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400   transition-all col-span-6
                            text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400 h-11""", "oninput" : "this.value = this.value.replace(/[^0-9]/g, '')"}),
            "des" : forms.TextInput(attrs={"placeholder" : "توضیخات", "class" : """block w-full py-1.5 px-3 text-base outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400   transition-all col-span-12 h-11
                            text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400""" }),
            
        }