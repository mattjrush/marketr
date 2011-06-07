import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response
from survey.models import Survey

def home(request):
    today = datetime.date.today()
    active = Survey.objects.active()
    completed = Survey.objects.completed().filter(closes__gte=today- datetime.timedelta(14))
    upcoming = Survey.objects.upcoming().filter(opens__lte=today+datetime.timedelta(7))
    return render_to_response('survey/home.html', 
        {'active_surveys': active,
         'completed_surveys':completed,
         'upcoming_surveys': upcoming})
    
def survey_detail(request, pk):
    return HttpResponse("This is the survey detail page for survey, " "with pk=%s" % pk)
