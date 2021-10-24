from django import template

register = template.Library()
from ..models import ArticlePost


# 除有默认的模板标签外，Django为了应对更多复杂的操作，还允许开发者自定义模板标签。
# Django中一共有三种自定义模板标签类型，分别是simple_tag、inclusion_tag和assignment_tag(不常用)。

# simple_tag
@register.simple_tag
def total_articles():
    # 注意这个地方是 每个登录的用户 必须要看见所有的文章 所有直接查询这个数据库的文章总数就可以了
    # 要是查询自己的 加条件就是的了
    #  ArticlePost.objects.filter(author=1).count() 这样加就是的拉

    return ArticlePost.objects.count()


@register.simple_tag
def author_total_articles(user):  # 这个user不用传递 因为在模板里面调用这个标签的user就会传递的
    return user.article.count()

#  自定义过滤器就不说了 把 {xxx|函数名(前面是函数的参数)}

#  这个地方你得先创建这个html 然后把你需要用这个模板创建的html 实现什么都写上
#  然后在其他文件中用这个 先引入 然后直接用  然后传递参数  {% latest_articles 4 %}
#  实际上这个模板语法 先去找刚刚创建html把他拿过来放这 这个4就是自定义的模板标签函数的参数
#  具体的就是这样的一个用法 多理解  inclusion包含
#  或者说你在你需要用的页面写上了这个模板标签 传递参数 会调用这个函数 然后这个数据给了你刚刚创建的html页面
#  完成渲染之后 放到你需要用的页面上了
@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    #  这个语法就不需要说了吧
    latest_articles = ArticlePost.objects.order_by("-created")[:n]
    return {"latest_articles": latest_articles}
