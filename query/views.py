from django.shortcuts import render
from query.models import PGRData
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import json

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
		dict0 = {"name":i.name,"city":i.city,"type":i.type,"pk":i.user.pk,"desc":i.desc}
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
	
