from django.conf.urls import include, url
from django.contrib import admin
from common.views import login, index, switch
from django.contrib.auth.views import logout

from schedules.views import schedule
from device_group.views import group
from thermometer.views import thermometers

urlpatterns = [

    url(r'^$', view=index, name="index"),
    url(r'^schedule/$', view=schedule, name="schedule"),
    url(r'^thermometers/$', view=thermometers, name="thermometers"),
    url(r'^group/(?P<group_name>[^/]+)/$', view=group, name="group"),
    url(r'^api/switch/(?P<pk>[0-9]+)/(?P<button_pk>[^/]+)/$', view=switch, name="switch"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, {'template_name': 'common/login.html'}),
    url(r'^accounts/logout/$', logout),
]
