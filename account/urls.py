from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    # path('login/', views.user_login,name='user_login'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login2.html'), name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='user_logout'),
    path('register/', views.register, name='user_register'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change_form.html',
                                                                   success_url='/account/password-change-done/'),
         name='password_change'),
    path('password-change-done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'),
         name='password_change_done'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name="account/password_reset_form.html",  # 重置密码的前端页面
             # 设置向申请重置密码的用户邮箱所发送的邮件内容  你看不见这个页面 默认就执行发送 使用里面的路径 或者说里面就是这样写的
             email_template_name="account/password_reset_email.html",
             success_url='/account/password-reset-done/'),  # 成功 页面跳转目标
         name='password_reset'),
    path('password-reset-done/',   # 这个地方就是邮件发送之后显示的页面
         auth_views.PasswordResetDoneView.as_view(
             template_name="account/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',  # 邮件发送过来 之后 有个连接 然后我们点击这个连接 本地还得访问这个页面 这就是
         auth_views.PasswordResetConfirmView.as_view(  # 这里面完成具体的重置
             template_name="account/password_reset_confirm.html",
             success_url='/account/password-reset-complete/'),
         name="password_reset_confirm"),
    path('password-reset-complete/',  # 重置完成展示的页面
         auth_views.PasswordResetCompleteView.as_view(
             template_name="account/password_reset_complete.html"),
         name="password_reset_complete"
         ),
    path('my-information/',views.myself,name="my_information"),
    path('edit-my-information/',views.myself_edit,name="edit_my_information")
]
