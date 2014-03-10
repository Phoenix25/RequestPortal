"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize registration behavior, feel free to set up
your own URL patterns for these views instead.

"""


from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

#from accounts.views import AccountActivationView as ActivationView
from accounts.views import AccountRegistrationView as RegistrationView
from accounts.views import PGRAccountEditView, UserAccountEditView, PGRAccountDetailView, UserAccountDetailView, UploadView, UploadLists
from accounts import views
urlpatterns = patterns('',
						# the following 4 views are by registration module for handling activation and registration
						url(r'^activate/complete/$',
                           TemplateView.as_view(template_name='registration/activation_complete.html'),
                           name='registration_activation_complete'),
						   
						url(r'^register/$',
                           RegistrationView.as_view(),	# link to RegistrationView(alias of AccountRegistrationView) in accounts.views. it's a modified version of the django-registration module's RegistrationView
                           name='registration_register'),
						
						# templates for the following view's do not exist yet. they are only static pages. create them after design is decided.
						url(r'^register/complete/$',
                           TemplateView.as_view(template_name='registration/registration_complete.html'),
                           name='registration_complete'),
						   
						url(r'^register/closed/$',
                           TemplateView.as_view(template_name='registration/registration_closed.html'),
                           name='registration_disallowed'),
						   
						(r'', include('registration.auth_urls')),	# include auth_urls from the registration framework for handling login,logout and password change.
						
						url(r'^edit/$',	# link to the show_profile function. The show_profile function checks the user group(i.e. whether customer or photographer) and presents the user (or) photographer account details whichever applies.
                           views.show_profile,
                           name='edit'),
						
						
						url(r'^detail_pgr/$',
                           PGRAccountDetailView.as_view(template_name='detail.html'),
                           name='detail_pgr'),
						
						# present account details for user
						url(r'^detail_user/$',
                           UserAccountDetailView.as_view(template_name='detail.html'),
                           name='detail_user'),
						
						url(r'^upload/$',
                           views.upload,
                           name='upload'),
						   
						url(r'^upload-list/$',
                           UploadLists.as_view(),
                           name='portfolio'),
						url(r'^master/$',
							'accounts.views.masterlogin',
							name='master_login'
							)
						
                       )
                       
						
                       