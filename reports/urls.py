from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.add_report, name='add_report'),
    url(r'^see/$', views.see_reports, name='see'),


    url(r'^folders/$', views.folders, name='folders'),
    url(r'^create_folder/$', views.create_folder, name='create_folder'),
    url(r'^folder/$', views.folder, name='folder'),
    url(r'^add_reports/(?P<folder_name>.+)$', views.add_reports, name='folder'),
    url(r'^savedReports/$', views.viewReportsInFolders, name='savedReports'),

    url(r'^MyReports/$', views.see_my_reports, name='see_my_reports'),
    url(r'^uploads/(?P<pk>\d+)/', views.download_file, name='download'),
    url(r'^edit/(?P<id>\d+)/$', views.edit_report, {}, name='report_edit'),
    url(r'^delete/(?P<id>\d+)/$', views.delete_report, {}, name='report_delete'),

]
