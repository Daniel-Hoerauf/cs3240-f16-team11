from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.add_report, name='add_report'),
    url(r'^thanks/$', views.thanks, name='thanks'),

]