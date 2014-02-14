from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from review.views import ReviewView,ReviewTokenList

urlpatterns = patterns('',
						# the following 4 views are by registration module for handling activation and registration
						url(r'^review/$',
                           ReviewView.as_view(),
                           name='review'),
						)