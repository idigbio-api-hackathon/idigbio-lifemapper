from django.conf.urls import url
from species import views

urlpatterns = [
    url(r'^species/$', views.SpeciesList.as_view()),
    url(r'^species/prefix/$', views.SpeciesPrefix.as_view()),
    url(r'^species/(?P<pk>.+)/$', views.SpeciesDetail.as_view()),
#    url(r'^species/$', views.species_list),
#    url(r'^species/(?P<pk>[0-9]+)/$', views.species_detail),
]
