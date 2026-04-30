from django.urls import path
from . import views

app_name = 'vulns'

urlpatterns = [
    # SQL 注入模块
    path('sqli/', views.sqli_home, name='sqli_home'),
    path('sqli/search/', views.sqli_search, name='sqli_search'),
    path('sqli/login/', views.sqli_login, name='sqli_login'),

    # XSS 模块
    path('xss/', views.xss_home, name='xss_home'),
    path('xss/post/', views.xss_post, name='xss_post'),

    # 文件上传模块
    path('upload/', views.upload_home, name='upload_home'),
    path('upload/do/', views.upload_do, name='upload_do'),

    # 命令注入模块
    path('cmd/', views.cmd_home, name='cmd_home'),
    path('cmd/ping/', views.cmd_ping, name='cmd_ping'),
]
