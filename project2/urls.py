from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^query/', include('query.urls', namespace='query')),
	url(r'^quote/', include('quote.urls', namespace='quote')),
	url(r'^accounts/', include('accounts.urls', namespace='accounts')),
	url(r'^index/', TemplateView.as_view(template_name="index_template.html"), name="index"),
)
