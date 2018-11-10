# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify,
#   * and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.urls import reverse


class CountryArea(models.Model):
	country_area_id = models.AutoField(primary_key=True)
	country_area_name = models.CharField(unique=True, max_length=100)
	m49_code = models.SmallIntegerField()
	iso_alpha3_code = models.CharField(max_length=3)
	location = models.ForeignKey('Location', models.DO_NOTHING)
	dev_status = models.ForeignKey('DevStatus', models.DO_NOTHING, blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'country_area'
		ordering = ['country_area_name']
		verbose_name = 'UNSD M49 Country or Area'
		verbose_name_plural = 'UNSD M49 Countries or Areas'

	def __str__(self):
		return self.country_area_name

	def get_absolute_url(self):
		return reverse('country_detail', args=[str(self.id)])


class DevStatus(models.Model):
	dev_status_id = models.AutoField(primary_key=True)
	dev_status_name = models.CharField(unique=True, max_length=25)

	class Meta:
		managed = False
		db_table = 'dev_status'
		ordering = ['dev_status_name']
		verbose_name = 'UNSD M49 Country or Area Development Status'
		verbose_name_plural = 'UNSD M49 Country or Area Development Statuses'

	def __str__(self):
		return self.dev_status_name


class HeritageSite(models.Model):
	heritage_site_id = models.AutoField(primary_key=True)
	site_name = models.CharField(unique=True, max_length=255)
	description = models.TextField()
	justification = models.TextField(blank=True, null=True)
	date_inscribed = models.IntegerField(blank=True, null=True)  # This field type is a guess.
	longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
	latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
	area_hectares = models.FloatField(blank=True, null=True)
	heritage_site_category = models.ForeignKey('HeritageSiteCategory', models.DO_NOTHING)
	transboundary = models.IntegerField()

	# Intermediate model (country_area -> heritage_site_jurisdiction <- heritage_site)
	country_area = models.ManyToManyField(CountryArea, through='HeritageSiteJurisdiction')

	class Meta:
		managed = False
		db_table = 'heritage_site'
		ordering = ['site_name']
		verbose_name = 'UNESCO Heritage Site'
		verbose_name_plural = 'UNESCO Heritage Sites'

	def __str__(self):
		return self.site_name

	def get_absolute_url(self):
		# return reverse('site_detail', args=[str(self.id)])
		return reverse('site_detail', kwargs={'pk': self.pk})

	@property
	def region_names(self):
		sort_order = ['location__region__region_name']
		countries = self.country_area.all().order_by(*sort_order)
		# countries_sorted = sorted(countries, key=lambda o: o.location.region.region_name)

		names = []
		for country in countries:
			region = country.location.region
			if region is None:
				continue
			name = region.region_name
			if name not in names:
				names.append(name)

		return ', '.join(names)

	@property
	def sub_region_names(self):
		sort_order = [
			'location__region__region_name',
			'location__sub_region__sub_region_name'
		]
		countries = self.country_area.all().order_by(*sort_order)

		names = []
		for country in countries:
			sub_region = country.location.sub_region
			if sub_region is None:
				continue
			name = sub_region.sub_region_name
			if name not in names:
				names.append(name)

		return ', '.join(names)

	@property
	def intermediate_region_names(self):
		sort_order = [
			'location__region__region_name',
			'location__sub_region__sub_region_name',
			'location__intermediate_region__intermediate_region_name'
		]
		countries = self.country_area.all().order_by(*sort_order)

		names = []
		for country in countries:
			intermediate_region = country.location.intermediate_region
			if intermediate_region is None:
				continue

			name = intermediate_region.intermediate_region_name
			if name not in names:
				names.append(name)

		return ', '.join(names)

	@property
	def country_area_names(self):
		sort_order = [
			'location__region__region_name',
			'location__sub_region__sub_region_name',
			'location__intermediate_region__intermediate_region_name',
			'country_area_name'
		]
		countries = self.country_area.all().order_by(*sort_order)

		names = []
		for country in countries:
			name = country.country_area_name
			if name is None:
				continue
			iso_code = country.iso_alpha3_code

			name_and_code = ''.join([name, ' (', iso_code, ')'])
			if name_and_code not in names:
				names.append(name_and_code)

		return ', '.join(names)

	# Admin site column header (Throws error when @property decorator used
	# country_area_names.short_description = 'Country/Area'

	'''
	def country_area_display(self):
		"""Create a string for country_area. This is required to display in the Admin view."""
		return ', '.join(
			country_area.country_area_name for country_area in self.country_area.all()[:25])
	country_area_display.short_description = 'Country or Area'
	'''


class HeritageSiteCategory(models.Model):
	category_id = models.AutoField(primary_key=True)
	category_name = models.CharField(unique=True, max_length=25)

	class Meta:
		managed = False
		db_table = 'heritage_site_category'
		ordering = ['category_name']
		verbose_name = 'UNESCO Heritage Site Category'
		verbose_name_plural = 'UNESCO Heritage Site Categories'

	def __str__(self):
		return self.category_name


class HeritageSiteJurisdiction(models.Model):
	heritage_site_jurisdiction_id = models.AutoField(primary_key=True)
	heritage_site = models.ForeignKey(HeritageSite, models.DO_NOTHING)
	country_area = models.ForeignKey(CountryArea, models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'heritage_site_jurisdiction'
		ordering = ['heritage_site', 'country_area']
		verbose_name = 'UNESCO Heritage Site Jurisdiction'
		verbose_name_plural = 'UNESCO Heritage Site Jurisdictions'

	'''
	def get_absolute_url(self):
		return reverse('site_detail', args=[str(self.id)])
	'''


class IntermediateRegion(models.Model):
	intermediate_region_id = models.AutoField(primary_key=True)
	intermediate_region_name = models.CharField(unique=True, max_length=100)
	sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'intermediate_region'
		ordering = ['intermediate_region_name']
		verbose_name = 'UNSD M49 Intermediate Region'
		verbose_name_plural = 'UNSD M49 Intermediate Regions'

	def __str__(self):
		return self.intermediate_region_name


class Location(models.Model):
	"""
	New model based on Mtg 5 refactoring of the database.
	"""
	location_id = models.AutoField(primary_key=True)
	planet = models.ForeignKey('Planet', models.DO_NOTHING)
	region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)
	sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING, blank=True, null=True)
	intermediate_region = models.ForeignKey('IntermediateRegion', models.DO_NOTHING, blank=True,
	                                        null=True)

	class Meta:
		managed = False
		db_table = 'location'
		ordering = ['planet', 'region', 'sub_region', 'intermediate_region']
		verbose_name = 'UNSD M49 Location Hierarchy'
		verbose_name_plural = 'UNSD M49 Location Hierarchies'

	def __str__(self):
		if self.intermediate_region:
			return self.intermediate_region.intermediate_region_name
		elif self.sub_region:
			return self.sub_region.sub_region_name
		elif self.region:
			return self.region.region_name
		elif self.planet:
			return self.planet.unsd_name
		else:
			return 'error'

		''' Works but ugly
		return '{}  {}  {}  {}'.format(
			self.planet,
			self.region if self.region else '',
			self.sub_region if self.sub_region else '',
			self.intermediate_region if self.intermediate_region else '')
		'''


class Planet(models.Model):
	"""
	New model based on Mtg 5 refactoring of the database.
	"""
	planet_id = models.AutoField(primary_key=True)
	planet_name = models.CharField(unique=True, max_length=50)
	unsd_name = models.CharField(unique=True, max_length=50)

	class Meta:
		managed = False
		db_table = 'planet'
		ordering = ['planet_name']
		verbose_name = 'UNSD M49 Global'
		verbose_name_plural = 'UNSD M49 Globals'

	def __str__(self):
		return self.unsd_name


class Region(models.Model):
	"""
	New planet FK added per Mtg 5 refactoring of the database.
	"""
	region_id = models.AutoField(primary_key=True)
	region_name = models.CharField(unique=True, max_length=100)
	planet = models.ForeignKey(Planet, models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'region'
		ordering = ['region_name']
		verbose_name = 'UNSD M49 Region'
		verbose_name_plural = 'UNSD M49 Regions'

	def __str__(self):
		return self.region_name


class SubRegion(models.Model):
	sub_region_id = models.AutoField(primary_key=True)
	sub_region_name = models.CharField(unique=True, max_length=100)
	region = models.ForeignKey(Region, models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'sub_region'
		ordering = ['sub_region_name']
		verbose_name = 'UNSD M49 Subregion'
		verbose_name_plural = 'UNSD M49 Subregions'

	def __str__(self):
		return self.sub_region_name
