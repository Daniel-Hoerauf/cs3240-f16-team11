from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.add_report, name='add_report'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^see/$', views.see_reports, name='see'),


    url(r'^folders/$', views.folders, name='folders'),
    url(r'^create_folder/$', views.create_folder, name='create_folder'),
    url(r'^folder/$', views.folder, name='folder'),
    url(r'^add_reports/(?P<folder_name>.+)$', views.add_reports, name='folder'),
    url(r'^savedReports/$', views.viewReportsInFolders, name='savedReports'),
]
