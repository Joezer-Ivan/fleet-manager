from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^areas/$', views.areas_of_chennai,  name = 'areas_of_chennai'),
    url(r'^mtc/$', views.mtc,  name = 'mtc'),
    url(r'routes/$', views.Bus_route,  name = 'Bus_route'),
    url(r'^$', views.Choose_Location,  name = 'Choose_Location'),
    url(r'^api/$', views.CurrentLocationList.as_view()),
    url(r'^api/(?P<license_plate>[A-Z][A-Z][0-9][0-9][A-Z][A-Z][0-9][0-9][0-9][0-9])/$', views.CurrentLocationDetail.as_view()),
    #use replace any ' ' with '+' in the url. I dont know how to handle the '/' characters in the names of some of the stage names.
    url(r'^api/routes/(?P<source>[A-Z+.-]+)=(?P<dest>[A-Z+.-]+)/$', views.APIRouteGet, name = 'APIRouteGet'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
