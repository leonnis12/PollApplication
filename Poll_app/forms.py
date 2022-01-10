from django.forms import ModelForm
from django import forms
from .models import Poll,Quiz

class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option_one', 'option_two', 'option_three']
        widgets = {
            'question': forms.Textarea(attrs={'placeholder': 'Type your question here'}),
            'option_one': forms.TextInput(attrs={'placeholder': 'Option 1'}),
            'option_two': forms.TextInput(attrs={'placeholder': 'Option 2'}),
            'option_three': forms.TextInput(attrs={'placeholder': 'Option 3'}),
        }

class CreateQuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Type your quiz name here'}),
        }