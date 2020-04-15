from django.db import models
from django.contrib.auth.models import User


# from QuestionApp.models import Question

class Answer(models.Model):
    user = models.ForeignKey(User, related_name='answers', verbose_name='回答者', on_delete=models.CASCADE)
    # question = models.ForeignKey('Question', related_name='answers', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True, verbose_name='回答时间')
    answer_text = models.TextField(verbose_name='回答内容')  # 这里只有文本框需要添加能插入图片，附件功能

    def __str__(self):
        return self.answer_text
# Create your models here.
