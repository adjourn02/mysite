from django.conf.urls import url

from . import views

app_name = 'blogs'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<post_slug>[- \w]+)/$', views.blog, name='blog'),
    url(r'^contact/$', views.contact, name='contact'),
    #url(r'^thanks/$', views.thanks, name='thanks'),
]