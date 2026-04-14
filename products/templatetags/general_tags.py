from django.template import Library
from users.models import CostumUser 


register = Library()

@register.filter(name="to_thousand_filter")
def to_thousand_filter(value):
    if value:
        return f"{value:,}"
    else:
        return value
    

@register.simple_tag(name="get_city")
def get_city(request):
    if request.user.is_authenticated:
        if request.user.city:
            for city in CostumUser.CITY_CHOICES:
                if request.user.city == city[0]:
                    return city[1]
        else:
            return "آدرس خود را انتخاب کنید"
    else:
        city = request.session["city"] if request.session.get("city") else "آدرس خود را انتخاب کنید"
        return city


@register.filter(name="check_filtered")
def check_filtered(value, id_list):
    if str(value) in id_list:
        return True
    return False