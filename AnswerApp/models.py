from django.db import models
from django.contrib.auth.models import User
from QuestionApp.models import Question
from CategoryApp.models import Category


class AnswerModel(models.Model):
    author = models.ForeignKey(User, related_name='answers', verbose_name='回答者', on_delete=models.CASCADE)
    question = models.ForeignKey('QuestionApp.Question', related_name='answers',
                                 verbose_name='问题', on_delete=models.CASCADE)
    # category = models.ForeignKey('CategoryApp.Category', related_name='answers',
    #                             verbose_name='分区', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True, verbose_name='回答时间')
    # slug = models.SlugField(max_length=500)
    answer_text = models.TextField(verbose_name='回答内容')

    def __str__(self):
        return self.answer_text

    class Meta:
        ordering = ("pub_date", )

# Create your models here.
