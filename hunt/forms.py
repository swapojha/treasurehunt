from django import forms
from .models import Question

class answer_form(forms.Form):
    answer = forms.CharField(widget=forms.TextInput(attrs=dict(required=True,max_length=100,placeholder="Your answer: ")))
