from django.urls import re_path

from . import views

app_name = 'base'

urlpatterns = [
    re_path(r'^$', views.IndexView, name='index'),
    re_path(r'logout/$', views.LogoutView, name='logout'),

]
