from django.contrib import admin
from .models import Post, Author, Tag, Comment

# Register your models here.


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("caption",)
    search_fields = ("caption",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email_address")
    search_fields = ("first_name", "last_name", "email_address")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date", "slug")
    list_filter = ("author", "date", "tags")
    search_fields = ("title", "slug", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    ordering = ("-date",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "user_email", "post")
    list_filter = ("post", "user_name")
    search_fields = ("user_name", "user_email", "text")


# admin.site.register(Tag)
# admin.site.register(Post)
# admin.site.register(Author)
