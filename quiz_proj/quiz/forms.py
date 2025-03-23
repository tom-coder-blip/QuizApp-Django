from django import forms
from .models import Quiz
from .models import Question

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_option']

