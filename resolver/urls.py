from django.urls import path 
from . import views


urlpatterns=[
path('', views.index, name='index'), 
path('compute', views.compute, name='compute'),
path('compute_csv', views.compute_csv, name='compute_csv'),
path('compute_multi', views.compute_multi, name='compute_multi'),
path('linkDomain', views.linkDomain, name='linkDomain'),






]		