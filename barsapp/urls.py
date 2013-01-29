from django.conf.urls import patterns, include, url

urlpatterns = patterns('barsapp.views',
    url(r'^$', 'index'),

#    url(r'^(?P<bar_name>[a-z]+)/user-home$', 'user_home'),
    url(r'^(?P<bar_name>[a-z]+)/$', 'bar_home'),

    url(r'^logout/$', 'logout'),
    url(r'^(?P<bar_name>[a-z]+)/logout/$', 'logout'),
)
