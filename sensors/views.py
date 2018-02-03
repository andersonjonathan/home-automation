from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DHT11, Reading, NetworkSensor, MCP3008Channel


def sensors(request):
    return render(request, 'sensors/sensors.html', {'current_page': "Sensors"})


def sensor_readings(request, identities, mod=1):
    identity_list = identities.split(',')
    raw_readings = Reading.objects.filter(identity__in=identity_list).order_by('identity', 'timestamp')
    identity = identity_list[0]
    sensor_list = []
    readings = []
    last_values = []
    for idx, item in enumerate(raw_readings):
        if item.identity != identity:
            name = ''
            if 'NetworkSensor-' in identity:
                name = NetworkSensor.objects.get(pk=identity[14:]).name
            if 'MCP3008Channel-' in identity:
                name = MCP3008Channel.objects.get(pk=identity[15:]).name
            sensor_list.append({
                'name': name,
                'readings': readings
            })
            identity = item.identity
            readings = []
            last_values = []
        last_values.append(item.value)
        if idx % int(mod) == 0:
            readings.append({'timestamp': item.timestamp, 'value': sum(last_values) / float(len(last_values))})
            last_values = []
    name = ''
    if 'NetworkSensor-' in identity:
        name = NetworkSensor.objects.get(pk=identity[14:]).name
    if 'MCP3008Channel-' in identity:
        name = MCP3008Channel.objects.get(pk=identity[15:]).name
    sensor_list.append({
        'name': name,
        'readings': readings
    })
    return render(request, 'sensors/sensor_readings.html', {'current_page': "Sensors", "sensors": sensor_list})


@api_view(['GET'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def dht11(request):
    try:
        pk = int(request.query_params['pk'])
        device = DHT11.objects.get(pk=pk)
        return Response({
            "temperature": device.last_temperature,
            "humidity": device.last_humidity,
        })
    except KeyError:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)