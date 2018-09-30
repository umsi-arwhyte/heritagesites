from django.contrib import admin

import heritagesites.models as models


@admin.register(models.CountryArea)
class CountryAreaAdmin(admin.ModelAdmin):
	fields = [
		'country_area_name',
		(
			'region',
			'sub_region',
			'intermediate_region'
		),
		(
			'm49_code',
			'iso_alpha3_code',
		),
		'dev_status'
	]

	list_display = [
		'country_area_name',
		'region',
		'sub_region',
		'intermediate_region',
		'm49_code',
		'iso_alpha3_code',
		'dev_status'
	]

	list_filter = ['region', 'sub_region', 'intermediate_region', 'dev_status']
# admin.site.register(models.CountryArea)


@admin.register(models.DevStatus)
class DevStatusAdmin(admin.ModelAdmin):
	fields = ['dev_status_name']
	list_display = ['dev_status_name']
	ordering = ['dev_status_name']

# admin.site.register(models.DevStatus)


@admin.register(models.HeritageSite)
class HeritageSiteAdmin(admin.ModelAdmin):

	# formfield_overrides = {
	# 	models.TextField: {'widget': CKEditorWidget},
	# }

	# fields = [
	# 	'site_name',
	# 	'heritage_site_category',
	# 	'description',
	# 	'justification',
	# 	'date_inscribed',
	# 	(
	# 		'longitude',
	# 		'latitude'
	# 	),
	# 	'area_hectares',
	# 	'transboundary'
	# ]

	fieldsets = (
		(None, {
			'fields': (
				'site_name',
				'heritage_site_category',
				'description',
				'justification',
				'date_inscribed'
			)
		}),
		('Location and Area', {
			'fields': [
				(
					'longitude',
					'latitude'
				),
				'area_hectares',
				'transboundary'
			]
		})
	)

	list_display = (
		'site_name',
		'date_inscribed',
		'area_hectares',
		'heritage_site_category',
		'country_area_display'
	)

	list_filter = (
		# 'country_area',
		'heritage_site_category',
		'date_inscribed'
	)
# admin.site.register(models.HeritageSite)


@admin.register(models.HeritageSiteCategory)
class HeritageSiteCategoryAdmin(admin.ModelAdmin):
	fields = ['category_name']
	list_display = ['category_name']
	ordering = ['category_name']

# admin.site.register(models.HeritageSiteCategory)


@admin.register(models.IntermediateRegion)
class IntermediateRegionAdmin(admin.ModelAdmin):
	fields = ['intermediate_region_name', 'sub_region']
	list_display = ['intermediate_region_name', 'sub_region']
	ordering = ['intermediate_region_name']

# admin.site.register(models.IntermediateRegion)


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
	fields = ['region_name']
	list_display = ['region_name']
	ordering = ['region_name']
# admin.site.register(models.Region)


@admin.register(models.SubRegion)
class SubRegionAdmin(admin.ModelAdmin):
	fields = ['sub_region_name', 'region']
	list_display = ['sub_region_name', 'region']
	ordering = ['sub_region_name']

# admin.site.register(models.SubRegion)
