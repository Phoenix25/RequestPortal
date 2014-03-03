from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from review.models import Review,ReviewToken
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from query.context_processors import basic_pgr
from django.template import RequestContext
# Create your views here.

class ReviewTokenList(ListView):
	model = ReviewToken
	template_name = "review/tokenlist.html"
	def get_queryset(self):
		qs = super(ReviewTokenList, self).get_queryset()
		qs = qs.filter(user = self.request.user, active = 1)
		return qs

# public review list as seen by others under a photographer's page.
class ReviewListView(ListView):
	model = Review
	template_name = "review/reviewlist.html"
	context_object_name = "review_list"
	def get_queryset(self):	
		qs = super(ReviewListView, self).get_queryset()
		qs = qs.filter(pgr = User.objects.filter(pk = self.request.GET['pk'])[0])
		#import pdb;pdb.set_trace()
		return qs
	def get_context_data(self,**kwargs):
		ctx = super(ReviewListView, self).get_context_data(**kwargs)
		return RequestContext(self.request,ctx,processors=[basic_pgr])

class ReviewView(CreateView):
	model = Review
	template_name = "review/review.html"
	
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse("accounts:auth_login"))
			
		token = ReviewToken.objects.filter(pk = request.POST['pk'])[0]
		if not ( token.user == request.user and token.active == 1 ):
			raise PermissionDenied
		
		r = Review(desc = request.POST['desc'], rating = request.POST['rating'], title=request.POST['title'])
		r.source = request.user
		r.pgr = token.pgr
		r.save()
		token.active = 0
		token.save()
		return HttpResponse("Success")
		
	def get_context_data(self,**kwargs):
		ctx = super(ReviewView, self).get_context_data(**kwargs)
		ctx['token'] = self.request.GET['token']
		return ctx

def get_user_rating(user):
	reviews = Review.objects.filter(pgr = user)
	rating = 0
	for review in reviews:
		rating += int(review.rating)
		if not reviews.count == 0:
			return float(rating)/float(reviews.count())
		else:
			return -1