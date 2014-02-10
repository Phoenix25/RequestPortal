from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView

from registration.backends.simple.views import RegistrationView
from accounts.forms import DetailForm
from query.models import PGRData
from accounts.models import UserData
from django.core.exceptions import PermissionDenied,ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,Group
from django.http import HttpResponse

# Create your models here.

permission_lists = {'test':['pybb.add_post','pybb.view_post']}

class AccountRegistrationView(RegistrationView):
	form_class = DetailForm
	def register(self, request, **cleaned_data):
			
		user = super(AccountRegistrationView, self).register(request, **cleaned_data)
		user.groups.add(request.POST['group'])
		user_profile = []
		if self.request.POST["group"] == "1":
			user_profile = PGRData(user = user)
		elif self.request.POST["group"] == "2":
			user_profile = UserData(user = user)
		user_profile.save()
		return user
	def get_context_data(self, **kwargs):
		ctx = super(AccountRegistrationView, self).get_context_data(**kwargs)
		ctx["group"] = self.request.GET["group"]
		return ctx;
	def get_success_url(self, request, new_user):
		if self.request.POST["group"] == "1":
			#return reverse("accounts:edit_pgr")
			return reverse("query:base")
		elif self.request.POST["group"] == "2":
			#return reverse("accounts:edit_user")
			return reverse("query:base")
		else:
			raise ValidationError("User type invalid. Only valid values are 1:Photographer and 2:GeneralUser")
	
class PGRAccountEditView(UpdateView):
	model = PGRData

	fields = ['name','type','city','desc']
	template_name = "query/edit.html"
	
	def dispatch(self, request, *args, **kwargs):
		#if len(UserData.objects.filter(user=self.request.user)) == 0:
		#	return 
		
		if not self.request.user.is_authenticated:
			return redirect("accounts:login")
		else:
			return super(UpdateView, self).dispatch(request,*args,**kwargs)
	def post(self, request, *args, **kwargs):
		p = super(PGRAccountEditView, self).post(request, *args, **kwargs)
		return HttpResponse("success")
	def get_object(self, queryset=None):
		return PGRData.objects.filter(user=self.request.user)[0]
	
	def get_success_url(self):
		return reverse("query:base")

def show_profile(request,**kwargs):
		if Group.objects.filter(pk=1)[0] in request.user.groups.all():
			return PGRAccountEditView.as_view(**kwargs)(request)
		elif Group.objects.filter(pk=2)[0] in request.user.groups.all():
			return UserAccountEditView.as_view(**kwargs)(request)

class PGRAccountDetailView(DetailView):
	model = PGRData
	
	def get_object(self):
		obj = PGRData.objects.filter(user = User.objects.filter(pk = self.request.GET["pk"])[0])[0]
		return obj
	
class UserAccountDetailView(DetailView):
	model = UserData
	template_name = "query/edit.html"
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return reverse('auth_login')
		else:
			return super(UserAccountDetailView, self).dispatch(request,*args,**kwargs)
		
	def get_object(self):
		obj = UserData.objects.filter(user = self.request.user)[0]
		return obj
	
class UserAccountEditView(UpdateView):

	model = UserData
	fields = ['address']
	template_name = "query/edit.html"	
	def dispatch(self, request, *args, **kwargs):
		#if len(UserData.objects.filter(user=self.request.user)) == 0:
		#	return 
		
		if not self.request.user.is_authenticated:
			return redirect("auth_login")
		else:
			return super(UpdateView, self).dispatch(request,*args,**kwargs)
	
	def post(self, request, *args, **kwargs):
		super(UserAccountEditView, self).post(request, *args, **kwargs)
		return HttpResponse('success')
		
	def get_object(self, queryset=None):
		return UserData.objects.filter(user=self.request.user)[0]
	
	def get_success_url(self):
		return reverse("query:base")
		
