"""FeedBack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from django.conf.urls import url

from login import views
from boards import views as boards_views
urlpatterns = [
    path('admin/', admin.site.urls,name = 'admin'),
    path('index/',views.index,name = 'index'),
    path('login/',views.login, name = 'login'),
    path('register/',views.register, name = 'views_register'),
    path('logout/',views.logout,name = 'logout'),
    path('boards/',boards_views.home,name = 'boards_home'),
    path('create_course/',views.CreateCourse,name = 'create_course'),
    path('personal_center/',views.PersonalCenter,name = 'personal_center'),
    path('update/',views.Update,name = 'update'),
    re_path(r'^index/choose/(?P<pk>\d+)/$',views.choose_course,name = 'choose_course'),
    re_path(r'^course/(?P<pk>\d+)/$',views.Course,name = 'course'),
    re_path(r'^boards/(?P<pk>\d+)/$', boards_views.board_topics, name='board_topics'),
    re_path(r'^boards/(?P<pk>\d+)/new/$', boards_views.new_topic, name='new_topic'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', boards_views.topic_posts, name='topic_posts'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$',boards_views.reply_topic, name='reply_topic'),
    re_path(r'^course/(?P<pk>\d+)/homework/$',views.HomeworkList,name = 'homework_list'),
    re_path(r'^course/(?P<pk>\d+)/homework/new/$',views.Assign,name = 'new_homework'),
    re_path(r'^course/(?P<pk>\d+)/homework/(?P<homework_pk>\d+)/$',views.HomeworkContent,name = 'homework_content'),
    re_path(r'^course/(?P<pk>\d+)/homework/(?P<homework_pk>\d+)/submit/$',views.HomeworkSubmit,name = 'homework_submit'),

]
