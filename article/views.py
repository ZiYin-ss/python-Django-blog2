from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import ArticleColumn, ArticlePost
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse
from .forms import ArticleColumnForm, ArticlePostForm


@login_required(login_url='/account/login/')
@csrf_exempt  # 创建并显示文章栏目
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, 'article/column/article_column.html', {"columns": columns, "column_form": column_form})
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
        # post请求就会创建数据啊 先自己找找自己数据库有没有 然后再判断
        if columns:  # 假如有 就返回2 代表不要创建
            return HttpResponse("2")
        else:  # 这个是没有 要是没有 就创建这条数据 如果你要拿变量接收的话你还可以用这条数据
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse("1")


@login_required(login_url='/account/login/')
@require_POST  # 只接收post请求
@csrf_exempt  # 取消跨域  修改文章栏目
def rename_article_column(request):
    column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        # 就是原来的数据都可以修改 因为没有判断啊
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt  # 删除文章栏目
def del_article_column(request):
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/login')
@csrf_exempt  # 文章发布
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()  # 这个地方是把所有的 有关这个作者的栏目都给他了
        return render(request, "article/column/article_post.html", {"article_post_form": article_post_form,
                                                                    "article_columns": article_columns})


@login_required(login_url='/account/login')
def article_list(request):
    articles = ArticlePost.objects.filter(author=request.user)
    return render(request, "article/column/article_list.html", {"articles": articles})
