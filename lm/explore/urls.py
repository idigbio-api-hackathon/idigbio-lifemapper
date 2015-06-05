from django.conf.urls import url

from . import views

urlpatterns = [
    # Ex:  /map/
    url(r'^$', views.individualcount, name='individualcount'),
    url(ur'^individualcount/$', views.individualcount, name='individualcount'),
    url(ur'^download/$', views.download, name='download'),
]

