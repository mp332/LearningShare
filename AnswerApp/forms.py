from django import forms
from django.contrib.auth.models import User
from .models import AnswerModel


class AnswerForm(forms.Form):
    class Meta:
        model = AnswerModel
        fields = ("question", "answer_text")
