from django.contrib import admin
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from .models import Slider, Product, Color, Category, Comment, ProductFileManager, Feature, AmazingOfferMain


class CategorySimpleListFilter(admin.SimpleListFilter):
    title = "category"
    parameter_name = "category"

    def lookups(self, request, model_admin):
        return [
            (category.pk, category.name) for category in Category.objects.filter(sub_cat=None)
        ]

    def queryset(self, request, queryset):
        return queryset.filter(category__id__in=[self.value()]) if self.value() else queryset


class FileInProduct(admin.TabularInline):
    model = ProductFileManager
    fields = ["title", "image", "upload_file_btn"]
    extra = 1
    readonly_fields = ["upload_file_btn"]

    def upload_file_btn(self, obj):
        return mark_safe(render_to_string("products/admin/upload_btn.html", {"obj": obj}))


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
    readonly_fields = ["price_after_off", "product_script"]
    list_filter = [CategorySimpleListFilter, "price",
                   "off", "price_after_off", "inventory"]
    filter_horizontal = ["category"]
    inlines = [FileInProduct, CommentInLine, FeaturInLine]
    ordering = ["-date_created"]

    def product_script(self, obj):
        return mark_safe("""
    <script src="/static/js/jquery.min.js"></script>
<script>
    timeout= null
    $(".upload-file-btn").on("click", function(e) {
        e.preventDefault()
        let fileId = $(this).data("file-id")
        let progressBar = $(".progress-bar" + fileId).find(".bar")
        console.log(fileId , progressBar ,progressBar[0].style.width + 10 )
        clearTimeout(timeout)
        timeout = setTimeout(() => {
            progressBar.css("width", progressBar[0].style.width + 10)
        }, 100)
    });
</script>
""")


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
