from django import forms
from django.contrib.auth.models import User
from .models import AnswerModel, Comment


class AnswerForm(forms.Form):
    # answer_text = forms.CharField(label='请输入问题内容(2000字以内):', max_length=2000, required=True,
    #                               widget=forms.Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = AnswerModel
        fields = ("question", "answer_text")


class CommentForm(forms.Form):
    comment_text = forms.CharField(label='请评论：', max_length=2000, required=True,
                                   widget=forms.Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Comment
        fields = ("commenter", "pub-time", "comment_text")
