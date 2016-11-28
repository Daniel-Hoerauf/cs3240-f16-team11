from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register_page, name='register_page'),
    url(r'^create_account/$', views.create_account, name='create_account'),
    url(r'^home/$', views.home, name='home'),
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^create_group/$', views.create_group, name='create_group'),
    url(r'^group/$', views.group, name='group'),
    url(r'^add_member/$', views.add_member, name='add_member'),
    url(r'^site_manager/$', views.site_manager, name='site_manager'),
    url(r'^give_SM_status/$', views.give_SM_status, name='give_SM_status'),
    url(r'^delete_member/$', views.delete_member, name='delete_member'),
]