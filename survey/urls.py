from django.conf.urls.defaults import *

urlpatterns = patterns('survey.views',
                       url(r'^$', 'home', name='survey_home'),
                       url(r'^(?P<pk>\d+)/$', 'survey_detail', name='survey_detail'),
)