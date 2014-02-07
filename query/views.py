from django.shortcuts import render
from query.models import PGRData
from django.http import HttpResponse
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
def city_pgr_view(request):
	all_pgrs = PGRData.objects.all()
	city = request.GET['city']
	filtered = []
	
	if not request.user.is_authenticated:
		return reverse('accounts:login')
	
	if not validate_city(city):
		city_pgr_fail(request, 'City name is invalid. Please enter a valid city name.')
	
	city_alias_list = get_alias_group(city)
	
	
	for city_item in city_alias_list:
		for pgr_item in PGRData.objects.filter(city=city_item):
			filtered.append(pgr_item)
	#if request.is_ajax():
	return HttpResponse(json.dumps(to_json(filtered)), mimetype = "text/json");
		
	# fill render command
	#return render(request, 'query/main.html', {'pgr_list':filtered})
	
