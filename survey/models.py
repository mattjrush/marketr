# -*- encoding: utf-8 -*-
import datetime
from django.db import models
from django.db.models import Max

class SurveyManager(models.Manager):
    def completed(self):
        return self.filter(closes__lt=datetime.date.today())
    def active(self):
        return self.filter(opens__lte=datetime.date.today()).filter(closes__gte=datetime.date.today())
    def upcoming(self):
        return self.filter(opens__gt=datetime.date.today())

class Survey(models.Model):
    title = models.CharField(max_length=60)
    opens = models.DateField()
    closes = models.DateField(blank=True)

    objects = SurveyManager()

    def save(self, **kwargs):
        """
        save override to allow for Survey instances to be created without
        explicitly specifying a closes date. If not specified, closes will
        be set to 7 days after opens.

        >>> t = "New Year's Resolutions"
        >>> sd = datetime.date(2009, 12, 28)
        >>> s = Survey.objects.create(title=t, opens=sd)
        >>> s.closes
        datetime.date(2010, 1, 4)
        """
        if not self.pk and self.opens and not self.closes:
            self.closes = self.opens + datetime.timedelta(7)
        super(Survey, self).save(**kwargs)

    def __unicode__(self):
        """
        >>> t = '¿Como está usted?'.decode('utf-8')
        >>> sd = datetime.date(2009, 12, 28)
        >>> s = Survey.objects.create(title=t, opens=sd)
        >>> print s
        ¿Como está usted? (opens 2009-12-28, closes 2010-01-04)
        """
        return u'%s (opens %s, closes %s)' % (self.title, self.opens, self.closes)
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('survey-detail', args=(self.pk))

class Question(models.Model):
    question = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey)

    def winning_answers(self):
        rv = []
        max_votes = self.answer_set.aggregate(Max('votes')).values()[0]
        if max_votes and max_votes > 0:
            rv = self.answer_set.filter(votes=max_votes)
        else:
            rv = self.answer_set.none()
        return rv
    
    def __unicode__(self):
        return u'%s: %s' % (self.survey, self.question)

class Answer(models.Model):
    answer = models.CharField(max_length=200)
    question = models.ForeignKey(Question)
    votes = models.IntegerField(default=0)