"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog import views
from django.views.static import serve
from BBS import settings
urlpatterns = [
    # 放到最上面或者中间,都不合适
    # url(r'^(?P<username>[\w]+)', views.user_blog),
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^get_valid_code/', views.get_valid_code),
    url(r'^register/', views.register),
    url(r'^check_username/', views.check_username),
    url(r'^index/', views.index),
    url(r'^logout/', views.logout),
    # 有名分组
    # url第一个参数正则表达式,第二个参数,函数的内存地址,第三个参数:字典,它会以关键字参数的形式,传到(第二个参数的)函数中,第四个参数,别名
    # 当你从浏览器输入:media/后面的路径回去settings.MEDIA_ROOT这个变量对应的文件夹下去寻找
    url(r'^media/(?P<path>.*)', serve,{'document_root':settings.MEDIA_ROOT}),

    # # 个人站点过滤分类的路由
    # url(r'^(?P<username>[\w]+)/category/(?P<category_id>\d+)', views.user_blog),
    # # 个人战点,标签过滤的路由
    # url(r'^(?P<username>[\w]+)/tag/(?P<tag_id>\d+)', views.user_blog),
    # # 随笔档案的路由(又得写好多)
    # # url(r'^(?P<username>[\w]+)/tag/(?P<tag_id>\d+)', views.user_blog),

    # 点赞的路由
    url(r'^diggit/$', views.diggit),
    # p评论的路由
    url(r'^commit_content/$', views.commit_content),



    # 三个过滤(分类,标签,归档),走一条路由
    # 分组分出三个(用户名,category|tag|archive中的一个,可能是分类id,tag_id,时间)
    url(r'^(?P<username>[\w]+)/(?P<condition>category|tag|archive)/(?P<param>.*)', views.user_blog),
    url(r'^(?P<username>[\w]+)/article/(?P<id>\d+)', views.article_detail),



    # 放到最后,都匹配完成,没有匹配到,再匹配它
    url(r'^(?P<username>[\w]+)$', views.user_blog),

]
