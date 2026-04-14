from django.contrib import admin

from .models import Slider, Product, Color, Category, Comment, ProductFileManager, Feature, AmazingOfferMain


class CategorySimpleListFilter(admin.SimpleListFilter):
    title = "category"
    parameter_name = "category"

    def lookups(self, request, model_admin):
        return [
            (category.pk, category.name) for category in Category.objects.filter(sub_cat=None)
        ]

    def queryset(self, request, queryset):
        return queryset.filter(category__id__in=[self.value()])



class FileInProduct(admin.TabularInline):
    model = ProductFileManager
    fields = ["title", "image"]
    extra = 1


class CommentInLine(admin.TabularInline):
    model = Comment
    fields = ["user", "title", "text", "status"]
    extra = 1


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ["title", "text", "date_created", "date_updated"]


class FeaturInLine(admin.TabularInline):
    model = Feature
    fields = ["name", "feature"]
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ["id", "name", "price",
                    "off", "price_after_off", "inventory"]
    search_fields = ["name"]
    readonly_fields = ["price_after_off"]
    list_filter = [CategorySimpleListFilter, "price", "off", "price_after_off", "inventory"]
    filter_horizontal = ["category"]
    inlines = [FileInProduct, CommentInLine, FeaturInLine]
    ordering = ["-date_created"]


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ["sub_cat", "name"]


class SliderAdmin(admin.ModelAdmin):
    model = Slider
    list_display = ["name", "image"]
    filter_horizontal = ["products"]


class AmazingAdminMain(admin.ModelAdmin):
    model = AmazingOfferMain
    filter_horizontal = ["products"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AmazingOfferMain, AmazingAdminMain)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Color)
admin.site.register(Comment, CommentAdmin)
