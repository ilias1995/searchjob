from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	url(r'^job/', 'apps.forms.views.job', name='job'),
	url(r'^(?P<jobtype_id>\d+)/$', 'apps.forms.views.jobtypes', name="jobtypes"),
	url(r'^$', 'apps.forms.views.index', name='index'),
	url(r'^addjob/', 'apps.forms.views.addjob', name='addjob'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^forms/', include('apps.forms.urls', namespace='forms')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^accounts/reset/done/$',
             'django.contrib.auth.views.password_reset_complete'),
    # Examples:
    # url(r'^$', 'searchjob.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
