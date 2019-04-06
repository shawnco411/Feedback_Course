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
    re_path(r'^index/(?P<pk>\d+)/$',views.Course,name = 'course'),
    re_path(r'^boards/(?P<pk>\d+)/$', boards_views.board_topics, name='board_topics'),
    re_path(r'^boards/(?P<pk>\d+)/new/$', boards_views.new_topic, name='new_topic'),
]
