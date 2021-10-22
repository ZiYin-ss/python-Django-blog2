from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse
from .forms import ArticleColumnForm




@login_required(login_url='/account/login/')
@csrf_exempt
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
