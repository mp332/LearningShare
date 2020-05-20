from django import forms
from django.contrib.auth.models import User
from .models import Question, Category
import re


class AskForm(forms.Form):
    """
    class Meta:
         model = Question
         fields=('questionTitle', 'category', 'questionDescription')

    """
    category = forms.ChoiceField(choices=Category.objects.values_list('number', 'name'), required=True, widget=forms.RadioSelect)
    title = forms.CharField(label='请输入问题题目(60字以内):', max_length=60,required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    #question = forms.CharField(label='请输入问题内容(2000字以内):', max_length=2000, required=True,widget=forms.Textarea(attrs={"class":"form-control"}))
    
    def clean_category(self):
        category = self.cleaned_data.get('category')
        return category

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 3:
            raise forms.ValidationError("Your title must be at least 3 characters long.")
        elif len(title) > 60:
            raise forms.ValidationError("Your title is too long.")
        else:
            filter_result = Question.objects.filter(questionTitle__exact=title)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your title already exists.")
        return title
    """
    def clean_question(self):
        question = self.cleaned_data.get('question')

        if len(question) < 3:
            raise forms.ValidationError("Your text must be at least 3 characters long.")
        elif len(question) > 2000:
            raise forms.ValidationError("Your text is too long.")
        else:
            return question
    """


