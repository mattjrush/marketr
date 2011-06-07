import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
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
    survey = get_object_or_404(Survey, pk=pk)
    today = datetime.date.today()
    if survey.closes < today:
        return display_completed_survey(request, survey)
    elif survey.opens > today:
        raise Http404
    else:
        return display_active_survey(request, survey)
    
def display_completed_survey(request, survey):
    return render_to_response('survey/completed_survey.html',
                              {'survey':survey})
    
def display_active_survey(request, survey):    
    return render_to_response('survey/active_survey.html', 
                              {'survey':survey})

    