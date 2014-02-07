from django.shortcuts import render
from django.views.generic.edit import FormView
from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import PermissionDenied
from quote.models import QuoteRequest
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class QuoteForm(forms.Form):
	desc = forms.CharField(max_length = '300', label = _("Event Description"))
	place = forms.CharField(max_length = '30', label = _("Event Location"))
	send_similar = forms.BooleanField(label = _("Send to 5 similar Photographers"))
	#target = forms.CharField(max_length = '5', label = _("Target(hidden)"))

class QuoteRequestView(FormView):
	template_name = 'quote/main.html'
	def get_context_data(self, **kwargs):
		ctx = super(QuoteRequestView, self).get_context_data(**kwargs)
		try:
			ctx['target'] = self.request.GET['target']
		except KeyError as e:
			raise PermissionDenied("TARGET_MISSING")
		return ctx
		
	def get_form_class(self):
		return QuoteForm
	
	def validate_pgr_id(self):
		return true
	
	def get_similar_pgrs(self,pgr):
		return [pgr]
	
	def redirect_login(self):
		raise PermissionDenied("Not logged in")
	
	def dispatch(self,request,*args,**kwargs):
		if not request.user.is_authenticated:
			redirect_login()
		return super(QuoteRequestView,self).dispatch(request,*args,**kwargs)
	
	def do_quote(self, request, quote):
		pass
	
	def post(self, request, *args, **kwargs):
		pgr = request.POST['target']
		similar = [pgr]
		"""try:
			if request.POST['send_similar']:
				similar = get_simiar_pgrs(pgr)
		except KeyError as e:
			raise PermissionDenied("send_similar field missing")"""
		
		for pgr_id in similar:
			q = QuoteRequest()
			q.desc = request.POST['desc']
			q.location = request.POST['place']
			q.source = request.user
			q.target = User.objects.filter(pk = pgr_id)[0]
			q.save()
			self.do_quote(request, q)
			
		return super(QuoteRequestView, self).post(request,*args,**kwargs)
		
	def get_success_url(self):
		return reverse("quote:success")
		
	
		
