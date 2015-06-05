from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = patterns('lm',
    # Examples:
    # url(r'^$', 'lm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(router.urls)),
    url(r'^', include('species.urls')),
    url(r'^map/', include('map.urls')),
    url(r'^explore/', include('explore.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^apiauth/', include('rest_framework.urls', namespace='rest_framework'))
)
