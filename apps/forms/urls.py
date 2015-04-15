from django.conf.urls import patterns, include, url
from django.contrib.auth import views


urlpatterns = patterns('',
	url(r'^registeration/', 'apps.forms.views.register', name='register'),
	url(r'^pravila/', 'apps.forms.views.pravila', name='pravila'),
	url(r'^login/$', 'apps.forms.views.login', name='login'),
	url(r'^base/', 'apps.forms.views.base', name='base'),
	url(r'^(?P<id>\d+)/$', 'apps.forms.views.info', name='info'),
	url(r'^(?P<job_id>\d+)/vote/$', 'apps.forms.views.vote', name='vote'),
	url(r'^logout/$','apps.forms.views.user_logout', name='logout'),
	url(r'^profile/$','apps.forms.views.profile', name='profile'),
	url(r'^cart/$', 'apps.forms.views.get_cart', name='cart'),
    url(r'^profile/(?P<id>\d+)/$', 'apps.forms.views.delete', name='delete'),
    url(r'^editprofile/$', 'apps.forms.views.update_profile', name='update_profile'),
    url(r'^password_change/$', 'apps.forms.views.password_change'),
    url(r'^change_success/$', 'apps.forms.views.change_success'),
    url(r'^password_reset/$', 'apps.forms.views.password_reset',
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset" ),
    url(r'^password_reset_confirm/$', 'apps.forms.views.password_reset_confirm'),
    url(r'^password_reset_done/$', 'apps.forms.views.password_reset_done'),
    # Examples:
    # url(r'^$', 'searchjob.views.home', name='home'),
)