from django.shortcuts import render
from django.views.generic.edit import UpdateView
# Create your views here.

from registration.backends.simple.views import RegistrationView
from accounts.forms import DetailForm
from query.models import PGRData as UserData
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your models here.

permission_lists = {'test':['pybb.add_post','pybb.view_post']}

class AccountRegistrationView(RegistrationView):
	form_class = DetailForm
	def register(self, request, **cleaned_data):
		
		#if(User.objects.filter(email=cleaned_data['email']).count() != 0):
		#	raise PermissionDenied("X") # redirect to.
			
		#if(User.objects.filter(username=cleaned_data['username']).count() != 0):
		#	raise PermissionDenied("Y") # redirect to.
			
		user = super(AccountRegistrationView, self).register(request, **cleaned_data)
		#user.groups.add(cleaned_data['group'])
		user_profile = UserData(user = user)
		user_profile.save()
		return user
	
	def get_success_url():
		return reverse("accounts:edit")

	
class AccountEditView(UpdateView):

	model = UserData
	fields = ['name','type','city','desc']
	template_name = "registration/registration-form.html"
	
	def dispatch(self, request, *args, **kwargs):
		#if len(UserData.objects.filter(user=self.request.user)) == 0:
		#	return 
		
		if not self.request.user.is_authenticated:
			return redirect("accounts:login")
		else:
			return super(UpdateView, self).dispatch(request,*args,**kwargs)
	
	def get_object(self, queryset=None):
		return UserData.objects.filter(user=self.request.user)[0]
	
	def get_success_url(self):
		return reverse("pybb:edit_profile")