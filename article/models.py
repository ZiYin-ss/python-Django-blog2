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
    # 如果文章是英文 然后url其他任何地方都不用变 传slug得时候 直接article.slug就传过去了 中文要管
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, on_delete=models.CASCADE, related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(User,related_name="articles_like",blank=True)

    class Meta:
        ordering = ("-updated",)
        index_together = (('id', 'slug'),)  # 建立索引

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        #  这个地方 这样写是因为 每一条数据 都会调用save方法 我们在前台写入的时候并不写入slug
        #  而是通过对title做改动保存下来的  然后再调用父类的save方法就是的了
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # 第二个参数就是 原本的url后面跟上文章的id和标题 /article/article-detail/1/Ni-Men-Huan-Hao-Ma/
        #  url.py去匹配
        #  这个reverse 就是把第一个参数 就是命名空间 第一个参数就相当于返回/article/article-detail/ href直接拿到跳转
        return reverse("article:article_detail", args=[self.id, self.slug])

    def get_url_path(self):
        return reverse("article:article_content", args=[self.id, self.slug])