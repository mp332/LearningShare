from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from QuestionApp.models import Question
from CategoryApp.models import Category


class AnswerModel(models.Model):
    author = models.ForeignKey(User, related_name='answers', verbose_name='回答者', on_delete=models.CASCADE)
    question = models.ForeignKey('QuestionApp.Question', related_name='answers',
                                 verbose_name='问题', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True, verbose_name='回答时间')
    answer_text = models.TextField(verbose_name='回答内容')
    goodNum = models.IntegerField(default=0, verbose_name='赞数')
    badNum = models.IntegerField(default=0, verbose_name='反对数')
    grade = models.IntegerField(default=0, verbose_name='综合质量')
    collect = models.ManyToManyField(User, related_name='collect_answer', verbose_name='收藏')
    user_like_answer = models.ManyToManyField(User, related_name='answers_like', blank=True)
    user_unlike_answer = models.ManyToManyField(User, related_name='answers_unlike', blank=True)

    def __str__(self):
        return self.answer_text

    class Meta:
        ordering = ("-grade",)

    def get_absolute_url(self):
        return reverse('question:question_content', kwargs={'question_id': self.question.id})


class Comment(models.Model):
    commenter = models.ForeignKey(User, related_name='comments', verbose_name='评论者', on_delete=models.CASCADE)
    answer = models.ForeignKey('AnswerModel', related_name='answer_comments', on_delete=models.CASCADE)
    comment_text = models.TextField(verbose_name='评论内容')
    pubDate = models.DateTimeField(auto_now=True, verbose_name='回答时间')
    goodNum = models.IntegerField(default=0)
    badNum = models.IntegerField(default=0)

    def __str__(self):
        return self.comment_text
