from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.add_report, name='add_report'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^see/$', views.see_reports, name='see')

]