from django.conf.urls import include, url
from django.contrib import admin
from common.views import login, index, switch, room
from django.contrib.auth.views import logout

from schedules.views import buttons
from sensors.views import sensors, sensor_readings, dht11
from radio.views import send_signals

urlpatterns = [
    url(r'^$', view=index, name="index"),
    url(r'^buttons/(?P<device_pk>[0-9]+)$', view=buttons, name="buttons"),
    url(r'^sensors/$', view=sensors, name="sensors"),
    url(r'^sensor/(?P<identities>[^/]+)/$', view=sensor_readings, name="sensor_readings"),
    url(r'^sensor/(?P<identities>[^/]+)/(?P<mod>[0-9]+)/$', view=sensor_readings, name="sensor_readings_mod"),
    url(r'^room/(?P<room_name>[^/]+)/$', view=room, name="room"),
    url(r'^api/switch/(?P<pk>[0-9]+)/(?P<button_pk>[^/]+)/$', view=switch, name="switch"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, {'template_name': 'common/login.html'}),
    url(r'^accounts/logout/$', logout),
    url(r'^api/radio/transmit', view=send_signals),
    url(r'^api/dht11', view=dht11)
]
