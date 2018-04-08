from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from schedule.models import Schedule, Ground, Division
from schedule.utils import schedule_matches


@csrf_exempt
def index(request):
    if request.POST:
        schedule_matches(request.POST.get('start_date'), request.POST.get('end_date'),
                         request.POST.getlist('exception_dates[]'))
        return HttpResponse("Success")
    return render(request, 'index.html', {})


def schedule(request):
    schedule = Schedule.objects.all().order_by('schedule_time')
    grounds = Ground.objects.all()
    divs = Division.objects.all()
    return render(request, 'schedule.html', {'schedules': schedule, 'grounds': grounds, 'divs': divs})
