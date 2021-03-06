from django.shortcuts import render
from query.models import PGRData
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from review.views import get_user_rating as get_rating
from django.views.generic.base import TemplateView
import json


class CityTemplateView(TemplateView):
	def get_context_data(self):
		ctx = super(CityTemplateView, self).get_context_data()
		ctx['city'] = self.request.GET['city']
		cities = []
		types = []
		for pgr in PGRData.objects.all():
			if pgr.city not in cities:
				cities.append(pgr.city)
			if pgr.type not in types:
				types.append(pgr.type)
		cities.remove(ctx['city'])
		ctx['cities'] = cities
		ctx['types'] = types
		return ctx
class HomeTemplateView(TemplateView):
	def get_context_data(self):
		ctx = super(HomeTemplateView, self).get_context_data()
		cities = []
		for pgr in PGRData.objects.all():
			if pgr.city not in cities:
				cities.append(pgr.city)
		ctx['cities'] = cities
		return ctx
# implement a validation mechanism
def validate_city(city):
	return 1
	
# implement a alias group mechanism for alternate names for a given city.
def get_alias_group(city):
	return [city]

# implement a failure page.
def city_pgr_fail(request, error):
	ctx = {'error': error }
	return render(request,"query/error.html", ctx)

def to_json(lst):
	res = []
	for i in lst:
		dict0 = {"name":i.name,"city":i.city,"type":i.type,"pk":i.user.pk,"desc":i.desc,"rating":get_rating(i.user),"avatar":i.avatar.url}
		res.append(dict0)
	return res
	
# to be called by background AJAX which directly replaces the obtained text in the main div.
# the view gets records of all photographers from a given city and returns them as json.
def city_pgr_view(request):
	all_pgrs = PGRData.objects.all()
	city = request.GET['city']
	filtered = []	# hold the filtered records
	
	if not request.user.is_authenticated:
		return reverse('auth_login')
	
	if not validate_city(city):
		city_pgr_fail(request, 'City name is invalid. Please enter a valid city name.')
	
	city_alias_list = get_alias_group(city)	#get aliases of a given city so as to not miss out on photographers
	
	
	# loop through all city names and append the records.
	for city_item in city_alias_list:
		for pgr_item in PGRData.objects.filter(city=city_item):
			filtered.append(pgr_item)
	
	return HttpResponse(json.dumps(to_json(filtered)), mimetype = "text/json");
	
