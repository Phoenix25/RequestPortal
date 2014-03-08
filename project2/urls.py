from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.contrib import admin
from query.views import HomeTemplateView
from project2 import settings
import accounts
import quote
import review
admin.autodiscover()


# the main url pattern matcher.
# use the namespace and name fields to reference a given view.
urlpatterns = patterns('',
	
    url(r'^admin/', include(admin.site.urls)),
	url(r'^query/', include('query.urls', namespace='query')),
	url(r'^quote/', include('quote.urls', namespace='quote')),
	url(r'^openid/',include('social_auth.urls')),
	url(r'^accounts/', include('accounts.urls', namespace='accounts')),
	url(r'^$', HomeTemplateView.as_view(template_name="homepage1.html"), name="index"),
	url(r'^review/', include('review.urls', namespace='review')),
	
	url(r'^pgrs/(?P<pk>\d+)/portfolio/(?P<page>\d+)/$',
                           accounts.views.UploadLists.as_view(),
                           name='portfolio'),
	url(r'^pgrs/(?P<target>\d+)/hire/',quote.views.QuoteRequestView.as_view(),
                           name='hire'),
	url(r'^pgrs/(?P<pk>\d+)/reviews/',review.views.ReviewListView.as_view(),
                           name='reviewlist'),
	
)+ static(settings.MEDIA_URL, document_root="")