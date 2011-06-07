import datetime
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