from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from radio.utils import transmit


@api_view(['POST'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def send_signals(request):
    """
    example:
    {
        "payload": "CABBABABAABABBABABAABABABBAABABBABABAABBAABABBAABBAABABBAABBABABAD",
        "signals": [
            {
                "char": "A",
                "on": 1,
                "off": 1
            },
            {
                "char": "B",
                "on": 1,
                "off": 5
            },
            {
                "char": "C",
                "on": 1,
                "off": 10
            }
            {
                "char": "D",
                "on": 1,
                "off": 40
            }
        ],
        "gpio": 4,
        "protocol_time": 0.00025,
        "rounds": 10
    }
    """
    try:
        transmitter_gpio = request.data['gpio']
        str_payload = request.data['payload'].replace(" ", "")
        signals = request.data['signals']
        rounds = request.data['rounds']
        t = request.data['protocol_time']
        payload = []
        for c in str_payload:
            on = None
            off = None
            for s in signals:
                if s['char'].lower() == c.lower():
                    on = s['on']
                    off = s['off']
                    break

            if on is not None:
                payload.append((1, on * t))
            if off is not None:
                payload.append((0, off * t))

        transmit(payload, transmitter_gpio, rounds)
        return Response(request.data)
    except KeyError:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)