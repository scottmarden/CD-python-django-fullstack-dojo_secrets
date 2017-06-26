from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^success$', views.success),
	url(r'^new_secret$', views.new_secret),
	url(r'^logout$', views.logout),
	url(r'^like$', views.like),
	url(r'^most_popular$', views.most_popular),
	url(r'^known_secrets$', views.known_secrets),
	url(r'^unknown_secrets$', views.unknown_secrets),
]
