from heritagesites.models import HeritageSite, HeritageSiteJurisdiction
from api.serializers import HeritageSiteSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


class SiteViewSet(viewsets.ModelViewSet):
	"""
	This ViewSet provides both 'list' and 'detail' views.
	"""
	queryset = HeritageSite.objects.select_related('heritage_site_category').order_by('site_name')
	serializer_class = HeritageSiteSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def delete(self, request, pk, format=None):
		"""
		This method performs the following operations:
		1) deletes all related M2M entries in the junction/associative heritage_site_jurisdiction
		table (this occurs first because of FK constraints) and
		2) deletes the HeritageSite instance from the heritage_site table.
		:param request:
		:param pk:
		:param format:
		:return:
		"""
		site = self.get_object(pk)

		# Setting the FK to on_delete.CASCADE renders this operation redundant
		# HeritageSiteJurisdiction.objects\
		# 	.filter(heritage_site_id__exact=site.heritage_site_id)\
		# 	.delete()

		# site.delete()
		self.perform_destroy(self, site)

		return Response(status=status.HTTP_204_NO_CONTENT)

	'''
	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		site_id = instance.heritage_site_id
		self.perform_destroy(self, instance)

		# Delete M2M HeritageSiteJurisdiction entries
		HeritageSiteJurisdiction.objects \
			.filter(heritage_site_id__exact=site_id) \
			.delete()

		# HeritageSite.objects \
		# 	.filter(heritage_site_id__exact=site_id) \
		# 	.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)
	'''

	def perform_destroy(self, instance):
		instance.delete()


'''
class SiteListAPIView(generics.ListCreateAPIView):
	queryset = HeritageSite.objects.select_related('heritage_site_category').order_by('site_name')
	serializer_class = HeritageSiteSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
'''

'''
class SiteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	queryset = HeritageSite.objects.select_related('heritage_site_category').order_by('site_name')
	serializer_class = HeritageSiteSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
'''
