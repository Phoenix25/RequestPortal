from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import PermissionDenied
from quote.models import QuoteRequest,Quote
from django.contrib.auth.models import User,Group
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import json

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
			self.redirect_login()
		else:
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
			
		ctx = super(QuoteRequestView, self).post(request,*args,**kwargs)
		return HttpResponse("Success")
		
	def get_success_url(self):
		return reverse("quote:success")
		
	
class QuoteDetailView(DetailView):
	model = Quote
	def get_object(self):
		return Quote.objects.filter(pk = self.request.GET['id'])[0]
	def dispatch(self, request, *args, **kwargs):
		
		if not self.request.user.is_authenticated:
			return redirect("accounts:login")
		
		if not Quote.objects.filter(pk = self.request.GET['id'])[0].user == self.request.user:
			raise PermissionDenied("Not Allowed")
		
		if "Photographer" in request.user.groups.all():
			self.template_name = "pgr-quote-detail.html"
		elif "General User" in request.user.groups.all():
			self.template_name = "user-quote-detail.html"
		
		
		return super(UpdateView, self).dispatch(request,*args,**kwargs)

class QuoteRequestDetailView(DetailView):
	model = QuoteRequest
	def get_object(self):
		return QuoteRequest.objects.filter(pk = self.request.GET['id'])[0]
	def dispatch(self, request, *args, **kwargs):
		
		if not self.request.user.is_authenticated:
			return redirect("accounts:login")
		
		if not QuoteRequest.objects.filter(pk = self.request.GET['id'])[0].source == self.request.user:
			raise PermissionDenied("Not Allowed")
			
		if Group.objects.filter(pk=1)[0] in request.user.groups.all():
			return PermissionDenied("Not Allowed")
		elif Group.objects.filter(pk=2)[0] in request.user.groups.all():
			self.template_name = "quote/user-quotereq-detail.html"
		
		
		return super(QuoteRequestDetailView, self).dispatch(request,*args,**kwargs)
		
def quote_to_json(lst, request):
	res = []
	for i in lst:
		dict0 = {"source":i.source,"target":i.target,"pk":i.pk,"desc":i.desc,"source_name":i}	# put necessary details only. further details will be communicated later. This is to reduce load times.
		res.append(dict0)
	return res

# view that returns a list of quotes associated with either 
"""def quote_list_view(self, reqeust):
	
	if not request.user.is_authenticated:	 #if it's an anonymous user, redirect to login.
		return reverse('login')
	
	
	filtered = 0
	if "Photographer" in request.user.groups.all():
		target = request.user					 # obtain the user object which is used for filtering the quote objects that we want to show.
		filtered = Quote.filter(target = target)
	else:
		source = request.user					 # obtain the user object which is used for filtering the quote objects that we want to show.
		filtered = Quote.filter(source = source)
	
	return HttpResponse(json.dumps(quote_to_json(filtered)), mimetype = "text/json");"""

class QuoteRequestListView(ListView):
	model = QuoteRequest
	context_object_name = "obj_list"
	
	def dispatch(self, request, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return redirect("accounts:login")
			
		if Group.objects.filter(pk=1)[0] in request.user.groups.all():
			return PermissionDenied("Not Allowed")
		elif Group.objects.filter(pk=2)[0] in request.user.groups.all():
			self.template_name = "quote/user-quotereq-list.html"
		else:
			raise PermissionDenied("Invalid group")
		return super(QuoteRequestListView, self).dispatch(request,*args,**kwargs)
	
	def get_queryset(self):
		qs = super(QuoteRequestListView, self).get_queryset()
		qs = qs.filter(source = self.request.user)
		return qs
	
class QuoteListView(ListView):
	model = Quote
	context_object_name = "obj_list"
	user_category = -1
	
	def dispatch(self, request, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return redirect("accounts:login")
			
		if "Photographer" in request.user.groups.all():
			self.template_name = "pgr-quote-list.html"
			user_category = 0
		elif "General User" in request.user.groups.all():
			self.template_name = "user-quote-list.html"
			user_category = 1
		return super(QuoteListView, self).dispatch(request,*args,**kwargs)
	
	def get_queryset(self):
		#qs = super(UpdateView, self).get_queryset()
		reqs = []
		if user_category == 0:
			reqs = QuoteRequest.objects.filter(target = self.request.user)
			
		elif user_category == 1:
			reqs = QuoteRequest.objects.filter(source = self.request.user)
		
		quotes = []
		for i in reqs:
			q = Quote.objects.filter(request = i)
			if not (q.count() == 0):
				quotes.append(q[0])
		return quotes