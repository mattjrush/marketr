from django.contrib import admin
from survey.models import Survey, Question, Answer

class QuestionsInline(admin.TabularInline):
    model = Question
    extra = 4

class AnswersInline(admin.TabularInline):
    model = Answer

class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionsInline]

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswersInline]

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)