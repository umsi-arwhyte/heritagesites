from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from .models import HeritageSite, HeritageSiteCategory, Planet, Region


class IndexViewTest(TestCase):

	def test_view_route_redirection(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 302)


class HomeViewTest(TestCase):

	def test_view_route(self):
		response = self.client.get('/heritagesites/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_name(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'heritagesites/home.html')


class AboutViewTest(TestCase):

	def test_view_route(self):
		response = self.client.get('/heritagesites/about/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_fail(self):
		response = self.client.get('/about/')
		self.assertEqual(response.status_code, 404)

	def test_view_route_name(self):
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'heritagesites/about.html')


class RegionModelTest(TestCase):

	def setUp(self):
		Planet.objects.create(planet_name='Earth', unsd_name='World')
		planet = Planet.objects.get(pk=1)
		Region.objects.create(region_name='Africa', planet_id=planet.planet_id)

	def test_region_name(self):
		region = Region.objects.get(pk=1)
		expected_object_name = f'{region.region_name}'
		self.assertEqual(expected_object_name, 'Africa')


class RegionListViewTest(TestCase):

	def test_view_route(self):
		response = self.client.get('/heritagesites/regions/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_fail(self):
		response = self.client.get('/regions/')
		self.assertEqual(response.status_code, 404)

	def test_view_route_name(self):
		response = self.client.get(reverse('regions'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('regions'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'heritagesites/location.html')


class SiteModelTest(TestCase):

	def setUp(self):
		HeritageSiteCategory.objects.create(category_name='Cultural')
		category = HeritageSiteCategory.objects.get(pk=1)
		HeritageSite.objects.create(
			site_name='Cultural Landscape and Archaeological Remains of the Bamiyan Valley',
			heritage_site_category_id=category.category_id,
			description='The cultural landscape and archaeological remains of the Bamiyan Valley ...',
			justification='The Buddha statues and the cave art in Bamiyan Valley are ...',
			date_inscribed='2003',
			longitude='67.82525000',
			latitude='34.84694000',
			area_hectares='158.9265',
			transboundary=0)

	def test_site_name(self):
		site = HeritageSite.objects.get(pk=1)
		expected_object_name = f'{site.site_name}'
		self.assertEqual(expected_object_name, 'Cultural Landscape and Archaeological Remains of '
		                                       'the Bamiyan Valley')


class SiteListViewTest(TestCase):

	def test_view_route(self):
		response = self.client.get('/heritagesites/sites/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_fail(self):
		response = self.client.get('/sites/')
		self.assertEqual(response.status_code, 404)

	def test_view_route_name(self):
		response = self.client.get(reverse('sites'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('sites'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'heritagesites/site.html')

'''
class SiteDetailViewTest(TestCase):

	def setUp(self):
		HeritageSiteCategory.objects.create(category_name='Natural')
		category = HeritageSiteCategory.objects.get(pk=2)
		HeritageSite.objects.create(
			site_name='Cultural Landscape and Archaeological Remains of the Bamiyan Valley',
			heritage_site_category_id=category.category_id,
			description='The cultural landscape and archaeological remains of the Bamiyan Valley ...',
			justification='The Buddha statues and the cave art in Bamiyan Valley are ...',
			date_inscribed='2003',
			longitude='67.82525000',
			latitude='34.84694000',
			area_hectares='158.9265',
			transboundary=0)

	def test_view_route(self):
		response = self.client.get('/heritagesites/sites/2/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_fail(self):
		response = self.client.get('/sites/2/')
		self.assertEqual(response.status_code, 404)

	def test_view_route_name(self):
		response = self.client.get(reverse('site_detail'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('site_detail'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'heritagesites/site_detail.html')
'''