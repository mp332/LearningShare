from django import forms
from django.contrib.auth.models import User
from .models import Question
import re


class AskForm(forms.Form):
    category = forms.ChoiceField(label='请选择问题种类', choices=[(0,'物理'),(1,'数学'),(2,'语言'),(3,'金融')], required=True,
                                 widget=forms.RadioSelect)
    title = forms.CharField(label='请输入问题题目(60字以内):', max_length=60,required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    question = forms.CharField(label='请输入问题内容(2000字以内):', max_length=2000, required=True,widget=forms.Textarea(attrs={"class":"form-control"}))

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if int(category) < 0 or int(category) > 3:
            raise forms.ValidationError("你选择的模块不存在")
        return category

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 3:
            raise forms.ValidationError("Your title must be at least 3 characters long.")
        elif len(title) > 60:
            raise forms.ValidationError("Your title is too long.")
        else:
            filter_result = Question.objects.filter(question_title__exact=title)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your title already exists.")
        return title

    def clean_question(self):
        question = self.cleaned_data.get('question')

        if len(question) < 3:
            raise forms.ValidationError("Your text must be at least 3 characters long.")
        elif len(question) > 2000:
            raise forms.ValidationError("Your text is too long.")
        else:
            return question
