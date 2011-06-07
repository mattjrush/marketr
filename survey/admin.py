from django.contrib import admin
from survey.models import Survey, Question, Answer
from django import forms

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
    def clean(self):
        opens = self.cleaned_data.get('opens')
        closes = self.cleaned_data.get('closes')
        if opens and closes and opens > closes:
            raise forms.ValidationError("Opens date cannot come after closes date.")
        return self.cleaned_data 
class QuestionsInline(admin.TabularInline):
    model = Question
    extra = 4

class AnswersInline(admin.TabularInline):
    model = Answer

class SurveyAdmin(admin.ModelAdmin):
    form = SurveyForm
    inlines = [QuestionsInline]

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswersInline]

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)

