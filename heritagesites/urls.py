from django.urls import path, re_path
from heritagesites import views

# RegEx paths
# https://simpleisbetterthancomplex.com/references/2016/10/10/url-patterns.html
# re_path(r'^sites/[0-9]+/$', views.SiteDetailView.as_view(), name='site_detail'),
'''
# app_name = 'heritagesites'
urlpatterns = [
    re_path(r'^$', views.HomePageView.as_view(), name='home'),
    re_path(r'^about/', views.AboutPageView.as_view(), name='about'),
    re_path(r'^locations/', views.LocationListView.as_view(), name='locations')
    re_path(r'^sites/', views.SiteListView.as_view(), name='sites'),
    re_path(r'^sites/(?P<pk>\d+)/$', views.SiteDetailView.as_view(), name='site_detail'),
]
'''

# app_name = 'heritagesites'
urlpatterns = [
	path('', views.HomePageView.as_view(), name='home'),
	path('about/', views.AboutPageView.as_view(), name='about'),
	path('countries/', views.CountryAreaListView.as_view(), name='country_area'),
	path('countries/<int:pk>/', views.CountryAreaDetailView.as_view(), name='country_area_detail'),
	path('locations/', views.LocationListView.as_view(), name='location'),
	path('oceania/', views.OceaniaListView.as_view(), name='oceania'),
	path('sites/', views.SiteFilterView.as_view(), name='site'),
	# path('sites/', views.SiteListView.as_view(), name='site'),
	path('sites/new/', views.SiteCreateView.as_view(), name='site_new'),
	path('sites/<int:pk>/', views.SiteDetailView.as_view(), name='site_detail'),
	path('sites/<int:pk>/delete/', views.SiteDeleteView.as_view(), name='site_delete'),
	path('sites/<int:pk>/update/', views.SiteUpdateView.as_view(), name='site_update'),
]
