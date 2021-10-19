from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_title,name='blog_title'),
    # 这个东西是匹配的是int形式的路由 同时这个article_id参数就是匹配的这个路由 传递进这个视图函数   get和post是请求 从request中拿出来的
    path('<int:article_id>/', views.blog_article,name='blog_article')
]
