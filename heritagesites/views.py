from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import HeritageSite, Region


def index(request):
	return HttpResponse("Hello, world. You're at the UNESCO Heritage Sites index page.")


class AboutPageView(generic.TemplateView):
	template_name = 'heritagesites/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'heritagesites/home.html'


class RegionListView(generic.ListView):
	model = Region
	context_object_name = 'regions'
	template_name = 'heritagesites/region.html'

	def get_queryset(self):
		return Region.objects.all()


class RegionDetailView(generic.DetailView):
	model = Region
	context_object_name = 'region'
	template_name = 'heritagesites/region_detail.html'


class SiteListView(generic.ListView):
	model = HeritageSite
	context_object_name = 'sites'
	template_name = 'heritagesites/site.html'
	paginate_by = 50

	def get_queryset(self):
		return HeritageSite.objects.all().select_related('heritage_site_category').order_by('site_name')
		# return HeritageSite.objects.all()

		'''
		return HeritageSite.objects.all().select_related('heritage_site_category').values_list(
			'site_name',
			'heritage_site_category__category_name',
			'description',
			'justification',
			'date_inscribed',
			'longitude',
			'latitude',
			'area_hectares').order_by('site_name')
		'''

		# 1168 records
		'''
		return HeritageSite.objects.select_related('heritage_site_category').values_list(
			'heritage_site_id',
			'site_name',
			'heritage_site_category__category_name',
			'description',
			'justification',
			'date_inscribed',
			'longitude',
			'latitude',
			'area_hectares',
			'country_area__country_area_name',
			'country_area__m49_code',
			'country_area__iso_alpha3_code',
			'country_area__dev_status__dev_status_name',
			'country_area__location__region__region_name',
			'country_area__location__sub_region__sub_region_name',
			'country_area__location__intermediate_region__intermediate_region_name').order_by('site_name')
		'''

class SiteDetailView(generic.DetailView):
	model = HeritageSite
	context_object_name = 'site'
	template_name = 'heritagesites/site_detail.html'
