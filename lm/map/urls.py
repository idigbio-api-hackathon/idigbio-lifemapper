from django.conf.urls import url

from . import views

urlpatterns = [
    # Ex:  /map/
    url(r'^$', views.index, name='index'),
    url(ur'^tutorial/$', views.tutorial, name='tutorial'),
    # Ex: /map/peromyscus%20maniculatus/
    url(ur'(?P<species>.+?)/$', views.detail, name='detail'),
]
