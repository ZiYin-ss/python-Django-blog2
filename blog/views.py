from django.shortcuts import render, get_object_or_404

from .models import BlogArticles


def blog_title(request):
    blogs = BlogArticles.objects.all()  # 再说一遍 你查询打印出来的是对象实例 因为定义了__str__方法 当你调用打印实例 调用str方法
    return render(request, 'blog/titles.html', {"blogs": blogs})


def blog_article(request, article_id):
    # article = BlogArticles.objects.get(id=article_id)   为什么用下面的写法呢 当网页不存在的时候 会显示错误
    # 这个东西是包裹在模型类外面的 当请求对象不存在是 会抛出异常  第一个参数是默许了 第二个参数是查询条件 可以多个
    article = get_object_or_404(BlogArticles, id=article_id)
    # pub = article.publish   "publish": pub,  不像做复杂的操作了
    return render(request, 'blog/content.html', {"article": article})
