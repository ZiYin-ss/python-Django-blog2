from django.db import models
from django.utils import timezone  # 这个类是用来生成时间的 现在时间
from django.contrib.auth.models import User   # 这个地方是连接到管理员表  有几个管理员 就可根据管理员添加文章

class BlogArticles(models.Model):
    title = models.CharField(max_length=30)
    #  related_name 这个就是允许类User的实例(也就是某个用户名) 以"blog_posts"属性反向查询到类 BlogArticles的实例
    #  换句话说可以 就是连接查询 查寻这个用户名下的文章信息
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="blog_posts")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        #  这个地方说过了 就是出版时间要倒序排序 你想啊 默认升序 就是说最开始的会在最上面 现在要最新的在上面
        ordering = ("-publish",)
        db_table = 'blog'

    def __str__(self):
        return u'Blog-Articles:%s' % self.title