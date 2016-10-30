from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register_page, name='register_page'),
    url(r'^create_account/$', views.create_account, name='create_account'),
    url(r'/report/form.html', 'auth_views.report_form_upload', name='report_form_upload'),
]
