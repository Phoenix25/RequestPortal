

from django import forms
from django.utils.translation import ugettext_lazy as _
import datetime
from django.contrib.auth.models import User


# form with fields for user/photographer registration.
class DetailForm(forms.Form):
	# basic data.
	
	
	username = forms.RegexField(regex=r'^[\w.@+-]+$', max_length=30, label=_("Username"), error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
	email = forms.EmailField(label=_("E-mail"))
	password1 = forms.CharField(widget=forms.PasswordInput, label=_("Password"))
	password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"))
	
	# clean username checks for validity of username. it's automatically called by the generic view.
	# in this particular implementation we check for uniqueness of username.
	def clean_username(self):
		if(User.objects.filter(username=self.cleaned_data['username']).count() != 0):
			raise forms.ValidationError(_("Duplicate User IDs"))
		return self.cleaned_data['username']
	
	# clean is a general function again automatically called by the generic view to perform validation.
	# in this particular implementation we check for uniqueness of email.
	def clean(self):
		if(User.objects.filter(email=self.cleaned_data['email']).count() != 0):
			raise forms.ValidationError(_("Duplicate Email IDs"))
	
		return self.cleaned_data
	

class UploadForm(forms.Form):
	file = forms.FileField()