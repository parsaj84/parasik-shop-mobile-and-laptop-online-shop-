from django.contrib import admin

from .models import Post, Paragraph, Category, Comment, CostumUser, PostFileManager

class FileInLine(admin.TabularInline):
    model = PostFileManager
    fields = ["title","file", "image"]
    


class ParagraphInline(admin.TabularInline):
    model = Paragraph
    fields = ["title", "text", "image", "image_title"]

class CommentInLine(admin.TabularInline):
    model = Comment
    fields = ["title" , "text"]
    
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_editable = ["status"]
    list_display = ["id","author","title", "date_created",
                    "date_updated", "status", "author"]
    filter_vertical = ["categories"]
    raw_id_fields = ["author"]
    inlines = [ParagraphInline,FileInLine]
    search_fields = ["author__phone" , "title", "categories__title","paragraphs__text", "paragraphs__text"]


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ["sub_cat", "title", "des",
                    "avatar", "date_created", "date_updated"]
    raw_id_fields = ["sub_cat"]
    search_fields  = ["title", "post__title", "des"]
    list_filter = ["date_created", "date_updated"]

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
