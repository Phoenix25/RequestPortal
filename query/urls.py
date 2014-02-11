
from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
						url(r'^query/$',
                           'query.views.city_pgr_view',		# for /query/query redirect to the function views.city_pgr_view() which returns the list of photographers by city. Note that you have to send a GET parameter "city" with the name of the city.
                           name='pgr_view'),
						url(r'^base/$',
                           TemplateView.as_view(template_name="base.html"), # for query/base, return base.html
                           name='base'),   
                       )