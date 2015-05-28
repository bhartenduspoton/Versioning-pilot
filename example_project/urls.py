from django.conf import settings
from django.conf.urls import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.index', name="home"),
    url(r'^home$', 'main.views.home', name="project_data"),
    url(r'^upload$', 'main.views.upload', name="upload"),
    url(r'^project$', 'main.views.create_project', name="project"),
    url(r'^apiUpload/(?P<user_data_id>\d+)$', 'main.views.apiUpload', name="apiUpload"),
    url(r'^login$', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout$', 'django.contrib.auth.views.logout', name="logout"),
     url(r'^add_edit_effort/(?P<project_id>\d+)$', 'main.views.add_edit_effort', name='add_edit_effort'),
    url(r'^project/(?P<project_id>\d+)$', 'main.views.project_details', name='project_details'),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
                {'document_root': settings.MEDIA_ROOT}),)
    urlpatterns += staticfiles_urlpatterns()
