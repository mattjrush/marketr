import datetime
from django.test import TestCase
from django.contrib.auth.models import User 
from django.core.urlresolvers import reverse

class AdminSurveyTest(TestCase):
    def setUp(self):
        self.username = 'survey_admin'
        self.pw = 'pwpwpw'
        self.user = User.objects.create_user(self.username, '', self.pw)
        
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.assertTrue(self.client.login(username=self.username, password=self.pw),
            "Logging in user %s, pw %s failed." %(self.username, self.pw))
    def testAddSurveyError(self):
        post_data = {
            'title': u'Time Traveling',
            'opens':datetime.date.today(), 
            'closes':datetime.date.today() - datetime.timedelta(1),
            'question_set-TOTAL_FORMS': u'0',
            'question_set-INITIAL_FORMS': u'0',
        }
        response = self.client.post(
            reverse('admin:survey_survey_add'), post_data)
        self.assertContains(response,
            "Opens date cannot come after closes date.")
        
    def testAddSurveyOK(self):
        post_data = {
            'title': u'Time Traveling',
            'opens':datetime.date.today(), 
            'closes':datetime.date.today(),
            'question_set-TOTAL_FORMS': u'0',
            'question_set-INITIAL_FORMS': u'0',
        }
        response = self.client.post(
            reverse('admin:survey_survey_add'), post_data)
        self.assertRedirects(response, reverse('admin:survey_survey_changelist'))
        