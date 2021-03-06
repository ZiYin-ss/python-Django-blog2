from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticleColumn, ArticlePost
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    #  这个地方就是说 以article:{}:views作为key 其实意思就是访问一次这个页面 就会执行一下这个函数 就是把这个key+1
    #  不同的文章的key不一样
    #  这样的话不就可以统计访问次数了吗
    total_views = r.incr("article:{}:views".format(article.id))
    r.zincrby('article_ranking', 1, article.id)  # 这个地方不知道是什么意思 真的不知道
    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    # article_ranking_ids 这个列表里面是id 文章的id
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    #  这个地方就是文章表里面的id在article_ranking_ids这个里面的位置 依据这个排序 假如1和2 key=1key=2 就排序出来就是1，2
    #  这个地方多理解 用的少肯定知道的少
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    return render(request, "article/list/article_content.html",
                  {"article": article,
                   "total_views": total_views,
                   "most_viewed": most_viewed})


def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title, 2)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    if username:
        return render(request, "article/list/author_articles.html",
                      {"articles": articles, "page": current_page,
                       "userinfo": userinfo, "user": user})

    return render(request, "article/list/article_titles.html",
                  {"articles": articles, "page": current_page})


@csrf_exempt
@require_POST
@login_required(login_url='/account/login/')
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")
