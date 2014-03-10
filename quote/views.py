from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import PermissionDenied
from quote.models import QuoteRequest,Quote
from query.models import PGRData
from django.contrib.auth.models import User,Group
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import json

# a form model for requesting a quote
class QuoteForm(forms.Form):
	desc = forms.CharField(max_length = '300', label = _("Event Description"))
	desc.widget.attrs['class'] = 'form-control'
	place = forms.CharField(max_length = '30', label = _("Event Location"))
	place.widget.attrs['class'] = 'form-control'
	send_similar = forms.BooleanField(label = _("Send to 5 similar Photographers"))
	#send_similar.widget.attrs['class'] = 'form-control'
	#target = forms.CharField(max_length = '5', label = _("Target(hidden)"))
	def __init__(self,*args,**kwargs):
		super(QuoteForm, self).__init__(*args, **kwargs)
		#self.desc.widget.attrs['class'] = 'form-control'
		#self.place.widget.attrs['class'] = 'form-control'
		#self.send_similar.widget.attrs['class'] = 'form-control'
	
# this view serves the form.
class QuoteRequestView(FormView):
	template_name = 'quote/quote-request.html'	# use the quote-request.html template
	
	
	# most of the following methods are overrides of FormView's methods when FormVIew attempts to dispatch the request,these functions will be called
	# put target id in the context so that the template can add a hidden input containing the id of the photographer.
	def get_context_data(self, **kwargs):
		ctx = super(QuoteRequestView, self).get_context_data(**kwargs)
		try:
			ctx['target'] = self.kwargs['target']
		except KeyError as e:
			raise PermissionDenied("TARGET_MISSING")
		ctx['pgr'] = PGRData.objects.filter(user = User.objects.filter(pk = self.kwargs['target'] ) [0] ) [0]
		return ctx
	
	#return the class representing the form
	def get_form_class(self):
		return QuoteForm
	
	# check if pgr_id is valid. currently unimplemented
	def validate_pgr_id(self):
		return true
	
	# utility function for finding similar photographers. currently unimplemented
	def get_similar_pgrs(self,pgr):
		return [pgr]
	
	def redirect_login(self):
		return redirect('accounts:master_login')
	
	# override the root method that is always called no matter what the request type.
	def dispatch(self,request,*args,**kwargs):
		# redirect to login if the user is not logged in.
		if not request.user.is_authenticated():
			return self.redirect_login()
		else:
			return super(QuoteRequestView,self).dispatch(request,*args,**kwargs)
	
	# function invoked each time a quote request is created. intended to send emails to moderators. currently unimplemented
	def do_quote(self, request, quote):
		pass
	
	# override post method to create the quote request
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
			q.date = request.POST['date']
			q.similar = request.POST['similar']
			q.event = request.POST['event']
			q.source = request.user	# 'source' refers to the customer
			q.target = PGRData.objects.filter(pk = pgr_id)[0].user # get the target Photographer object and assign it to the QuoteRequest record.
			q.save()
			self.do_quote(request, q)
			
		ctx = super(QuoteRequestView, self).post(request,*args,**kwargs)
		
		# currently return success as the output string since the receiver is expected to be using AJAX.
		return HttpResponse("Success")
		
	# not used if the request is based on AJAX.
	def get_success_url(self):
		return reverse("quote:success")
		
# this view sends details of a given quote after cheching if the user is either the source or the target of the quote
class QuoteDetailView(DetailView):
	model = Quote
	template_name = "quote/user-quote-detail.html"
	def get_object(self):
		return Quote.objects.filter(pk = self.request.GET['id'])[0]
	def dispatch(self, request, *args, **kwargs):
		
		if not self.request.user.is_authenticated:
			return redirect("accounts:login")
		
		# check if the user is allowed to see the quote(i.e. either the target or the source)
		if not ( Quote.objects.filter(pk = self.request.GET['id'])[0].req.source == self.request.user or Quote.objects.filter(pk = self.request.GET['id'])[0].req.target == self.request.user) :
			raise PermissionDenied("Not Allowed")
		
		# assign different templates to the target and the source so they can see a personalized version.
		if Group.objects.filter(pk=1)[0] in request.user.groups.all():
			self.template_name = "pgr-quote-detail.html"
		elif Group.objects.filter(pk=2)[0] in request.user.groups.all():
			self.template_name = "user-quote-detail.html"
		
		
		return super(QuoteDetailView, self).dispatch(request,*args,**kwargs)

# this view does the same thing as above but for the Quote Request object.
# additionaly it does not allow photographer users to view QuoteRequest objects.
class QuoteRequestDetailView(DetailView):
	model = QuoteRequest
	def get_object(self):
		return QuoteRequest.objects.filter(pk = self.request.GET['id'])[0]
	def dispatch(self, request, *args, **kwargs):
		
		if not self.request.user.is_authenticated:
			return redirect("socialauth_begin")
		
		if not QuoteRequest.objects.filter(pk = self.request.GET['id'])[0].source == self.request.user:
			raise PermissionDenied("Not Allowed")
			
		if Group.objects.filter(pk=1)[0] in request.user.groups.all():
			return PermissionDenied("Not Allowed")
		elif Group.objects.filter(pk=2)[0] in request.user.groups.all():
			self.template_name = "quote/user-quotereq-detail.html"
		
		
		return super(QuoteRequestDetailView, self).dispatch(request,*args,**kwargs)
	
# utility function for conversion of quote model to a json-friendly dict.
# currently not used but will be used if searching through quotes is necessary.
def quote_to_json(lst, request):
	res = []
	for i in lst:
		dict0 = {"source":i.source,"target":i.target,"pk":i.pk,"desc":i.desc}	# put necessary details only. further details will be communicated later. This is to reduce load times.
		res.append(dict0)
	return res

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

#Presents quote request objects as a list.
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
	
# similar to the above view but for quote objects.
class QuoteListView(ListView):
	model = Quote
	context_object_name = "obj_list"
	user_category = -1
	
	def dispatch(self, request, *args, **kwargs):
		#import pdb;pdb.set_trace()
		if not self.request.user.is_authenticated():
			return redirect("socialauth_begin",'facebook')
				
		if Group.objects.filter(pk=1)[0] in request.user.groups.all():
			self.template_name = "quote/pgr-quote-list.html"
			self.user_category = 0
		elif Group.objects.filter(pk=2)[0] in request.user.groups.all():
			self.template_name = "quote/user-quote-list.html"	# TODO: shift template to proper directory.
			self.user_category = 1
		return super(QuoteListView, self).dispatch(request,*args,**kwargs)
	
	def get_queryset(self):
		reqs = []
		if self.user_category == 0:
			reqs = QuoteRequest.objects.filter(target = self.request.user)
			
		elif self.user_category == 1:
			reqs = QuoteRequest.objects.filter(source = self.request.user)
		
		quotes = []
		for i in reqs:
			q = Quote.objects.filter(req = i)
			if not (q.count() == 0):
				quotes.append(q[0])
		return quotes