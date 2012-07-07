from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^/?$', 'jp.views.home'),
    url(r'^getjob/?$', 'jp.views.getjob'),
    url(r'^checkpoint/?$', 'jp.views.checkpoint'),
    url(r'^result/?$', 'jp.views.result'),
    url(r'^work/?$', 'jp.views.work'),
    url(r'^proof/?$', 'jp.views.proof'),
    url(r'^rainbow\.js/?$', 'jp.views.rainbow'),
    url(r'^getData\.js/?$', 'jp.views.getData'),
    url(r'^ajax/?$', 'jp.views.ajax'),
    url(r'^localStorage/?$', 'jp.views.localStorage'),
    url(r'^cross_localStorage/?$', 'jp.views.cross_localStorage'),
    # url(r'^$', 'mebro.views.home', name='home'),
    # url(r'^mebro/', include('mebro.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)