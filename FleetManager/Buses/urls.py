from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.areas_of_chennai,  name = 'areas_of_chennai'),
    url(r'^mtc/$', views.mtc,  name = 'mtc'),
    url(r'routes/$', views.Bus_route,  name = 'Bus_route'),
    url(r'^choice/$', views.Choose_Location,  name = 'Choose_Location'),

]
