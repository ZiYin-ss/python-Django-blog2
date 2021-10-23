from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify
from django.utils import timezone


class ArticleColumn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_column")
    column = models.CharField(max_length=200)
    create = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, on_delete=models.CASCADE, related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("title",)
        index_together = (('id', 'slug'),)  # 建立索引

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        #  这个地方 这样写是因为 每一条数据 都会调用save方法 我们在前台写入的时候并不写入slug
        #  而是通过对title做改动保存下来的  然后再调用父类的save方法就是的了
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.id, self.slug])
