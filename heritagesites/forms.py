from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from heritagesites.models import HeritageSite


class HeritageSiteForm(forms.ModelForm):
	class Meta:
		model = HeritageSite
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.add_input(Submit('submit', 'Submit'))


class SearchForm(forms.ModelForm):
	date_inscribed = forms.IntegerField(
		label='Date Inscribed',
		required=False
	)

	class Meta:
		model = HeritageSite
		fields = ['date_inscribed']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'GET'
		self.helper.add_input(Submit('submit', 'Search'))
