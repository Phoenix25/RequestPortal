from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.contrib import admin
from project2 import settings
admin.autodiscover()


# the main url pattern matcher.
# use the namespace and name fields to reference a given view.
urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
	url(r'^query/', include('query.urls', namespace='query')),
	url(r'^quote/', include('quote.urls', namespace='quote')),
	url(r'^accounts/', include('accounts.urls', namespace='accounts')),
	url(r'^index/', TemplateView.as_view(template_name="index_template.html"), name="index"),
)+ static(settings.MEDIA_URL, document_root="")
