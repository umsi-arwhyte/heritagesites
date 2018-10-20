from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.db.models import F, Q

from .models import HeritageSite, Location, Region


def index(request):
	return HttpResponse("Hello, world. You're at the UNESCO Heritage Sites index page.")


class AboutPageView(generic.TemplateView):
	template_name = 'heritagesites/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'heritagesites/home.html'


class LocationListView(generic.ListView):
	model = Location
	context_object_name = 'locations'
	template_name = 'heritagesites/location.html'

	def get_queryset(self):
		return Location.objects\
			.select_related('region', 'sub_region', 'intermediate_region')\
			.order_by('region__region_name',
		              'sub_region__sub_region_name',
		              'intermediate_region__intermediate_region_name'
		              )


class OceaniaListView(generic.ListView):
	model = HeritageSite
	context_object_name = 'sites'
	template_name='heritagesites/oceania.html'
	paginate_by = 10

	def get_queryset(self):
		return HeritageSite.objects\
			.select_related('heritage_site_category')\
			.filter(country_area__location__region__region_id = 5)\
			.order_by('country_area__location__sub_region__sub_region_name',
		              'country_area__country_area_name',
		              'site_name')

class SiteListView(generic.ListView):
	model = HeritageSite
	context_object_name = 'sites'
	template_name = 'heritagesites/site.html'
	paginate_by = 50

	def get_queryset(self):
		return HeritageSite.objects\
			.select_related('heritage_site_category')\
			.order_by('site_name')


class SiteDetailView(generic.DetailView):
	model = HeritageSite
	context_object_name = 'site'
	template_name = 'heritagesites/site_detail.html'
