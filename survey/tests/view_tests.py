import datetime
from django.test import TestCase
from survey.models import Survey

class SurveyTest(TestCase):
    def setUp(self):
        today = datetime.date.today()
        Survey.objects.all().delete()
        d = today - datetime.timedelta(15)
        Survey.objects.create(title="Too Old", opens=d, closes=d)
        d += datetime.timedelta(1)
        Survey.objects.create(title="Completed 1", opens=d, closes=d)
        d = today - datetime.timedelta(1)
        Survey.objects.create(title="Completed 2", opens=d, closes=d)
        Survey.objects.create(title="Active 1", opens=d)
        Survey.objects.create(title="Active 2", opens=today)
        d = today + datetime.timedelta(1)
        Survey.objects.create(title="Upcoming 1", opens=d)
        d += datetime.timedelta(6)
        Survey.objects.create(title="Upcoming 2", opens=d)
        d += datetime.timedelta(1)
        Survey.objects.create(title="Too Far Out", opens=d)
        
from django.core.urlresolvers import reverse
class SurveyDetailTest(SurveyTest):
    def testUpcoming(self):
        survey = Survey.objects.get(title='Upcoming 1')
        response = self.client.get(reverse('survey_detail', args=(survey.pk,)))
        self.assertEqual(response.status_code, 404)
        
    def testCompleted(self):
        survey = Survey.objects.get(title='Too Old')
        response = self.client.get(reverse('survey_detail', args=(survey.pk,)))
        self.assertTemplateUsed(response, 'survey/completed_survey.html')
    
    def testActive(self):
        survey = Survey.objects.get(title='Active 1')
        response = self.client.get(reverse('survey_detail', args=(survey.pk,)))
        self.assertTemplateUsed(response, 'survey/active_survey.html')

class SurveyHomeTest(SurveyTest):
    def testHome(self):
        from django.core.urlresolvers import reverse
        response = self.client.get(reverse('survey_home'))
        self.assertNotContains(response, "Too Old")
        self.assertNotContains(response, "Too Far Out")
        context_vars = ['completed_surveys', 'active_surveys', 'upcoming_surveys']
        title_starts = ['Completed', 'Active', 'Upcoming']
        for context_var, title_start in zip(context_vars, title_starts):
            surveys = response.context[context_var]
            self.assertEqual(len(surveys), 2, 
                             "Expected 2 %s, found %d instead" % 
                             (context_var, len(surveys)))
            for survey in surveys:
                self.failUnless(survey.title.startswith(title_start),
                              "%s title %s does not start with %s" %
                              (context_var, survey.title, title_start))