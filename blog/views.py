from django.shortcuts import render

from .models import BlogArticles


def blog_title(request):
    blogs = BlogArticles.objects.all()  # 再说一遍 你查询打印出来的是对象实例 因为定义了__str__方法 当你调用打印实例 调用str方法
    return render(request, 'blog/titles.html', {"blogs": blogs})


def blog_article(request, article_id):
    article = BlogArticles.objects.get(id=article_id)
    pub = article.publish
    return render(request, 'blog/content.html', {"publish": pub, "article": article})
