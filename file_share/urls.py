from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'file_share.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('web.urls')),
    url(r'^reports/', include('reports.urls')),
]
