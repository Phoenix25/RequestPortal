
from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView
urlpatterns = patterns('',
						url(r'^query/$',
                           'query.views.city_pgr_view',
                           name='pgr_view'),
						url(r'^base/$',
                           TemplateView.as_view(template_name="base.html"),
                           name='base'),   
                       )