from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.add_report, name='add_report'),
    url(r'^see/$', views.see_reports, name='see'),
    url(r'^uploads/(?P<pk>\d+)/', views.download_file, name='download'),

]
