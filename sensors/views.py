from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DHT11


def sensors(request):
    return render(request, 'sensors/sensors.html', {'current_page': "Sensors"})


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