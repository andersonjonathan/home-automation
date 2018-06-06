from django.urls import path, include
from django.contrib import admin
from common.views import login, index, switch, room, ApiEndpoint
from django.contrib.auth.views import logout
from schedules.views import buttons
from sensors.views import sensors, sensor_readings, dht11
from radio.views import send_signals

urlpatterns = [
    path('', view=index, name="index"),
    path('buttons/<int:device_pk>', view=buttons, name="buttons"),
    path('sensors/', view=sensors, name="sensors"),
    path('sensor/<str:identities>)/', view=sensor_readings, name="sensor_readings"),
    path('sensor/<str:identities>)/<int:mod>/', view=sensor_readings, name="sensor_readings_mod"),
    path('room/<str:room_name>/', view=room, name="room"),
    path('api/switch/<int:pk>/<int:button_pk>/', view=switch, name="switch"),
    path('admin/', admin.site.urls),
    path('accounts/login/', login, {'template_name': 'common/login.html'}),
    path('accounts/logout/', logout),
    path('api/radio/transmit', view=send_signals),
    path('api/dht11', view=dht11),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/hello', ApiEndpoint.as_view()),
]
