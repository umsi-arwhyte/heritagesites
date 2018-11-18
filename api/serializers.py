from heritagesites.models import CountryArea, DevStatus, HeritageSite, HeritageSiteCategory, \
	Location, Planet, Region, SubRegion, IntermediateRegion
from rest_framework import serializers


class PlanetSerializer(serializers.ModelSerializer):

	class Meta:
		model = Planet
		fields = ('planet_id', 'planet_name', 'unsd_name')


class RegionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Region
		fields = ('region_id', 'region_name', 'planet_id')


class SubRegionSerializer(serializers.ModelSerializer):

	class Meta:
		model = SubRegion
		fields = ('sub_region_id', 'sub_region_name', 'region_id')


class IntermediateRegionSerializer(serializers.ModelSerializer):

	class Meta:
		model = IntermediateRegion
		fields = ('intermediate_region_id', 'intermediate_region_name', 'sub_region_id')


class LocationSerializer(serializers.ModelSerializer):
	planet = PlanetSerializer(many=False, read_only=True)
	region = RegionSerializer(many=False, read_only=True)
	sub_region = SubRegionSerializer(many=False, read_only=True)
	intermediate_region = IntermediateRegionSerializer(many=False, read_only=True)

	class Meta:
		model = Location
		fields = ('location_id', 'planet', 'region', 'sub_region', 'intermediate_region')


class DevStatusSerializer(serializers.ModelSerializer):

	class Meta:
		model = DevStatus
		fields = ('dev_status_id', 'dev_status_name')


class CountryAreaSerializer(serializers.ModelSerializer):
	dev_status = DevStatusSerializer(many=False, read_only=True)
	location = LocationSerializer(many=False, read_only=True)

	class Meta:
		model = CountryArea
		fields = (
			'country_area_id',
			'country_area_name',
			'm49_code',
			'iso_alpha3_code',
			'dev_status',
			'location')


class HeritageSiteCategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = HeritageSiteCategory
		fields = ('category_id', 'category_name')


class HeritageSiteSerializer(serializers.ModelSerializer):
	country_area = CountryAreaSerializer(many=True, read_only=True)
	heritage_site_category = HeritageSiteCategorySerializer(many=False, read_only=True)

	class Meta:
		model = HeritageSite
		fields = (
			'heritage_site_id',
			'site_name',
			'heritage_site_category',
			'description',
			'justification',
			'date_inscribed',
			'longitude',
			'latitude',
			'area_hectares',
			'country_area',
			'transboundary'
		)
