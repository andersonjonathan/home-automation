from django.shortcuts import render


def thermometers(request):
    return render(request, 'thermometer/thermometers.html', {'current_page': "Thermometers"})
