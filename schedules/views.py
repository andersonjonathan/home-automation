from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from schedules.models import Schedule


@login_required
def schedule(request):
    context = {'current_page': 'Schedule',
               'schedules': Schedule.objects.all()}
    return render(request, 'schedules/schedule.html', context)
