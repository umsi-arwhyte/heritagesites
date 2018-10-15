from django.test.runner import DiscoverRunner


class UnManagedModelTestRunner(DiscoverRunner):
	"""
	A custom test runner for converting unmanaged models to managed before running a test
	and then revert the effect afterwards.

	Tell Django to use this runner by adding TEST_RUNNER setting to project settings.py
	TEST_RUNNER = 'app_name.utils.UnManagedModelTestRunner'

	Original: Tobias McNulty (now outdated)
	https://www.caktusgroup.com/blog/2010/09/24/simplifying-the-testing-of-unmanaged-database-models-in-django/

	Updated: Paul Vergeev
	https://dev.to/patrnk/testing-against-unmanaged-models-in-django

	Dependency: django-test-without-migrations
	https://pypi.org/project/django-test-without-migrations/

	Running
	$ python3 manage.py test -n (macOS)
	> python manage.py test --n (Windows)

	See also: https://stackoverflow.com/questions/18085245/running-tests-with-unmanaged-tables-in-django
	"""

	def setup_test_environment(self, *args, **kwargs):
		from django.apps import apps

		get_models = apps.get_models
		self.unmanaged_models = [m for m in get_models() if not m._meta.managed]

		for m in self.unmanaged_models:
			m._meta.managed = True

		super(UnManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)

	def teardown_test_environment(self, *args, **kwargs):
		super(UnManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)

		for m in self.unmanaged_models:
			m._meta.managed = False