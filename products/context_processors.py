from .models import Category

def category(request):
    return {"all_categories" : Category.objects.all() }


def sub_cats(request):

    return {"sub_cats" : Category.objects.filter(sub_cat=None)}

def saved_cat_id(request):
    if request.session.get("saved_cat_id"):
        return {"saved_cat" : Category.objects.get(pk=request.session.get("saved_cat_id"))}
    else:
        return {"saved_cat" : None}