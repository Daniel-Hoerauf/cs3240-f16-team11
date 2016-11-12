from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register_page, name='register_page'),
    url(r'^create_account/$', views.create_account, name='create_account'),
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^create_group/$', views.create_group, name='groups'),
]
