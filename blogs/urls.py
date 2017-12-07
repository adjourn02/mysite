from django.conf.urls import url

from . import views

app_name = 'blogs'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^place/(?P<place_id>[0-9]+)/$', views.blog, name='blog'),
]