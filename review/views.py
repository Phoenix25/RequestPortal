from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from review.models import Review,ReviewToken
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
# Create your views here.

class ReviewTokenList(ListView):
	model = ReviewToken
	template_name = "review/tokenlist.html"
	def get_queryset(self):
		qs = super(ReviewTokenList, self).get_queryset()
		qs = qs.filter(source = self.request.user, active = 1)
		return qs

class ReviewView(CreateView):
	model = Review
	template_name = "review/review.html"
	
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse("accounts:auth_login"))
			
		token = ReviewToken.objects.filter(pk = request.POST['pk'])[0]
		if not ( token.user == request.user and token.active == 1 ):
			raise PermissionDenied
		
		r = Review(desc = request.POST['desc'], rating = request.POST['rating'])
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