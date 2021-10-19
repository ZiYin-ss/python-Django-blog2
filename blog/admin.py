from django.contrib import admin

from .models import BlogArticles


class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish", "body")
    list_filter = ("publish", "author")
    search_fields = ("title", "body")
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ["-publish",'author']

admin.site.register(BlogArticles,BlogArticlesAdmin)  # 注册到admin中 此时就可以通过admin对模型类增删查改
