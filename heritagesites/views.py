from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from heritagesites.forms import HeritageSiteForm
from heritagesites.models import CountryArea, HeritageSite, HeritageSiteJurisdiction, Location


@login_required()
def index(request):
	return HttpResponse("Hello, world. You're at the UNESCO Heritage Sites index page.")


class AboutPageView(generic.TemplateView):
	template_name = 'heritagesites/about.html'


@method_decorator(login_required, name='dispatch')
class CountryAreaDetailView(generic.DetailView):
	model = CountryArea
	context_object_name = 'country'
	template_name = 'heritagesites/country_area_detail.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_object(self):
		country_area = super().get_object()
		return country_area


@method_decorator(login_required, name='dispatch')
class CountryAreaListView(generic.ListView):
	model = CountryArea
	context_object_name = 'countries'
	template_name = 'heritagesites/country_area.html'
	paginate_by = 20

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return CountryArea.objects.select_related('dev_status', 'location').order_by('country_area_name')


class HomePageView(generic.TemplateView):
	template_name = 'heritagesites/home.html'


class LocationListView(generic.ListView):
	model = Location
	context_object_name = 'locations'
	template_name = 'heritagesites/location.html'

	def get_queryset(self):
		return Location.objects \
			.select_related('region', 'sub_region', 'intermediate_region') \
			.order_by('region__region_name',
		              'sub_region__sub_region_name',
		              'intermediate_region__intermediate_region_name'
		              )


class OceaniaListView(generic.ListView):
	model = HeritageSite
	context_object_name = 'sites'
	template_name = 'heritagesites/oceania.html'
	paginate_by = 10

	def get_queryset(self):
		return HeritageSite.objects \
			.select_related('heritage_site_category') \
			.filter(country_area__location__region__region_id=5) \
			.order_by('country_area__location__sub_region__sub_region_name',
		              'country_area__country_area_name',
		              'site_name')


class OceaniaDetailView(generic.DetailView):
	model = HeritageSite
	context_object_name = 'site'
	template_name = 'heritagesites/oceania_detail.html'

	def get_object(self):
		site = super().get_object()
		return site


@method_decorator(login_required, name='dispatch')
class SiteCreateView(generic.View):
	model = HeritageSite
	form_class = HeritageSiteForm
	success_message = "Heritage Site created successfully"
	template_name = 'heritagesites/site_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('heritagesites/site_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = HeritageSiteForm(request.POST)
		if form.is_valid():
			site = form.save(commit=False)
			site.save()
			for country in form.cleaned_data['country_area']:
				HeritageSiteJurisdiction.objects.create(heritage_site=site, country_area=country)
			return redirect(site) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(site.get_absolute_url())
		return render(request, 'heritagesites/site_new.html', {'form': form})

	def get(self, request):
		form = HeritageSiteForm()
		return render(request, 'heritagesites/site_new.html', {'form': form})


'''
class SiteCreateView(generic.CreateView):
	model = HeritageSite
	form_class = HeritageSiteForm
	template_name = 'heritagesites/site_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = ''

	def form_valid(self, form):
		site = form.save(False)
		site.save()
		for country in form.cleaned_data['country_area']:
			HeritageSiteJurisdiction.objects.create(heritage_site=site, country_area=country)
		return HttpResponseRedirect(site.get_absolute_url())
		#return HttpResponseRedirect(self.get_success_url())
'''


@method_decorator(login_required, name='dispatch')
class SiteDeleteView(generic.DeleteView):
	model = HeritageSite
	success_message = "Heritage Site deleted successfully"
	success_url = reverse_lazy('site')
	context_object_name = 'site'
	template_name = 'heritagesites/site_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete HeritageSiteJurisdiction entries
		HeritageSiteJurisdiction.objects \
			.filter(heritage_site_id=self.object.heritage_site_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())


class SiteDetailView(generic.DetailView):
	model = HeritageSite
	context_object_name = 'site'
	template_name = 'heritagesites/site_detail.html'

	def get_object(self):
		site = super().get_object()
		return site


class SiteListView(generic.ListView):
	model = HeritageSite
	context_object_name = 'sites'
	template_name = 'heritagesites/site.html'
	paginate_by = 50

	def get_queryset(self):
		return HeritageSite.objects \
			.select_related('heritage_site_category') \
			.order_by('site_name')


@method_decorator(login_required, name='dispatch')
class SiteUpdateView(generic.UpdateView):
	model = HeritageSite
	form_class = HeritageSiteForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'site'
	# pk_url_kwarg = 'site_pk'
	success_message = "Heritage Site updated successfully"
	template_name = 'heritagesites/site_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		site = form.save(commit=False)
		# site.updated_by = self.request.user
		# site.date_updated = timezone.now()
		site.save()

		# Current country_area_id values linked to site
		old_ids = HeritageSiteJurisdiction.objects\
			.values_list('country_area_id', flat=True)\
			.filter(heritage_site_id=site.heritage_site_id)

		# New countries list
		new_countries = form.cleaned_data['country_area']

		# TODO can these loops be refactored?

		# New ids
		new_ids = []

		# Insert new unmatched country entries
		for country in new_countries:
			new_id = country.country_area_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				HeritageSiteJurisdiction.objects \
					.create(heritage_site=site, country_area=country)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				HeritageSiteJurisdiction.objects \
					.filter(heritage_site_id=site.heritage_site_id, country_area_id=old_id) \
					.delete()

		return HttpResponseRedirect(site.get_absolute_url())
		# return redirect('heritagesites/site_detail', pk=site.pk)
