
from quote.views import QuoteRequestView,QuoteDetailView,QuoteRequestDetailView,QuoteRequestListView,QuoteListView
from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
                        url(r'^quote/$',
                           QuoteRequestView.as_view(),
                           name='pgr_view'),
						url(r'^quote/success/$',
                           TemplateView.as_view(template_name='quote/success.html'),
                           name='success'),
						url(r'^qdetails/$',
                           QuoteDetailView.as_view(),
                           name='qdetail'),
						url(r'^qrdetails/$',
                           QuoteRequestDetailView.as_view(),
                           name='qrdetail'),
						url(r'^qrlist/$',
                           QuoteRequestListView.as_view(),
                           name='qrlist'),
						url(r'^qlist/$',
                           QuoteListView.as_view(),
                           name='qlist'),
                       )