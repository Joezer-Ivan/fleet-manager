from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.areas_of_chennai,  name = 'areas_of_chennai'),
    url(r'^mtc$', views.mtc,  name = 'mtc'),

]
