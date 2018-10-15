from django.urls import path, re_path
from . import views

# RegEx paths
# https://simpleisbetterthancomplex.com/references/2016/10/10/url-patterns.html
# re_path(r'^sites/[0-9]+/$', views.SiteDetailView.as_view(), name='site_detail'),
'''
# app_name = 'heritagesites'
urlpatterns = [
    re_path(r'^$', views.HomePageView.as_view(), name='home'),
    re_path(r'^about/', views.AboutPageView.as_view(), name='about'),
    re_path(r'^regions/', views.RegionListView.as_view(), name='regions'),
    re_path(r'^regions/(?P<pk>\d+)/$', views.RegionDetailView.as_view(), name='region_detail'),
    re_path(r'^sites/', views.SiteListView.as_view(), name='sites'),
    re_path(r'^sites/(?P<pk>\d+)/$', views.SiteDetailView.as_view(), name='site_detail'),
]
'''

# app_name = 'heritagesites'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('regions/', views.RegionListView.as_view(), name='regions'),
    path('regions/<int:pk>/', views.RegionDetailView.as_view(), name='region_detail'),
    path('sites/', views.SiteListView.as_view(), name='sites'),
    path('sites/<int:pk>/', views.SiteDetailView.as_view(), name='site_detail'),
]
