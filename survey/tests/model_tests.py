import datetime
from django.db import models
from django.test import TestCase
from django.db import IntegrityError
from survey.models import Survey

class SurveyUnicodeTest(TestCase):
    def testUnicode(self):
        t = u'Como esta usted?'
        sd = datetime.date(2009, 12, 28)
        s = Survey.objects.create(title=t, opens=sd)
        self.assertEqual(unicode(s),
                u'Como esta usted? (opens 2009-12-28, closes 2010-01-04)')

from survey.models import Question
class QuestionWinningAnswersTest(TestCase):
    
    fixtures = ['test_winning_answers.json']
    
    def testClearWinner(self):
        q = Question.objects.get(question='Clear Winner')
        wa_qs = q.winning_answers()
        self.assertEqual(wa_qs.count(), 1)
        winner = wa_qs[0]
        self.assertEqual(winner.answer, 'Max Votes')
        
    def testTwoWayTie(self):
        q = Question.objects.get(question ='2-Way Tie')
        wa_qs = q.winning_answers()
        self.assertEqual(wa_qs.count(), 2)
        for winner in wa_qs:
            self.assert_(winner.answer.startswith('Max Votes'))
            
    def testNoResponse(self):
        q = Question.objects.get(question = 'No Responses')
        wa_qs = q.winning_answers()
        self.assertEqual(wa_qs.count(), 0)
        
    def testNoAnswers(self):
        q = Question.objects.get(question = 'No Answers')
        wa_qs = q.winning_answers()
        self.assertEqual(wa_qs.count(), 0)
        
class SurveySaveTest(TestCase):
    t = "New Year's Resolutions"
    sd = datetime.date(2009, 12, 28)
    
    def testClosesAutoset(self):
        s = Survey.objects.create(title=self.t, opens=self.sd)
        self.assertEqual(s.closes, datetime.date(2010,1,4))
        
    def testClosesHonored(self):
        s = Survey.objects.create(title=self.t, opens=self.sd,closes=self.sd)
        self.assertEqual(s.closes, self.sd)
        
    def testClosesReset(self):
        s = Survey.objects.create(title=self.t, opens=self.sd)
        s.closes=None
        
        strict = True
        debug = False
        from django.conf import settings
        if 'mysql' in settings.DATABASES.get('default').get('ENGINE'):
            from django.db import connection
            c = connection.cursor()
            c.execute('SELECT @@SESSION.sql_mode')
            mode = c.fetchone()[0]
            if 'STRICT' not in mode:
                strict = False;
                from django.utils import importlib
                debug = importlib.import_module(
                        settings.SETTINGS_MODULE).DEBUG
                
        if strict:
            self.assertRaises(IntegrityError, s.save)
        elif debug:
            self.assertRaises(Exception, s.save)
        else:
            s.save()
            self.assertEqual(s.closes, None)
    
    def testTitleOnly(self):
        self.assertRaises(IntegrityError, Survey.objects.create,title=self.t)
        
class SurveyManagerTest(TestCase):
    def setUp(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(1)
        yesterday = today - oneday
        tomorrow = today + oneday
        Survey.objects.all().delete()
        Survey.objects.create(title="Yesterday", opens=yesterday, closes=yesterday)
        Survey.objects.create(title="Today", opens=today, closes=today)
        Survey.objects.create(title="Tomorrow", opens=tomorrow, closes=tomorrow)
        
    def testCompleted(self):
        self.assertEqual(Survey.objects.completed().count(), 1)
        completed_survey = Survey.objects.get(title="Yesterday")
        self.assertEqual(Survey.objects.completed()[0], completed_survey)
        
        today = datetime.date.today()
        completed_survey.closes = today
        completed_survey.save()
        self.assertEqual(Survey.objects.completed().count(), 0)
        
    def testActive(self):
        self.assertEqual(Survey.objects.active().count(), 1)
        active_survey = Survey.objects.get(title="Today")
        self.assertEqual(Survey.objects.active()[0], active_survey)
        yesterday = datetime.date.today() - datetime.timedelta(1)
        active_survey.opens = active_survey.closes = yesterday
        active_survey.save()
        self.assertEqual(Survey.objects.active().count(), 0)
    
    def testUpcoming(self):
        self.assertEqual(Survey.objects.upcoming().count(), 1)
        upcoming_survey = Survey.objects.get(title="Tomorrow")
        self.assertEqual(Survey.objects.upcoming()[0], upcoming_survey)
        yesterday = datetime.date.today() - datetime.timedelta(1)
        upcoming_survey.opens = yesterday
        upcoming_survey.save()
        self.assertEqual(Survey.objects.upcoming().count(), 0)