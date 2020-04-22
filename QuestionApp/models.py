# -*- coding: utf-8 -*-

from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from CategoryApp.models import Category

# Create your models here.


class Question(models.Model):
    user = models.ForeignKey(User, verbose_name='提问者', related_name='questions',on_delete=models.CASCADE)
    questionTitle = models.CharField('问题标题', max_length=40, unique=True,blank=False)
    questionCategory = models.ForeignKey('CategoryApp.Category', verbose_name='板块名称', on_delete=models.CASCADE)
    questionDescription = models.TextField('详细描述')
    created=models.DateTimeField(default=timezone.now,verbose_name='发布日期')
    publishDate = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    goodNum = models.IntegerField(default=0,verbose_name='赞数')
    badNum = models.IntegerField(default=0, verbose_name='反对数')
    grade = models.IntegerField(default=0, verbose_name='综合质量')
    collect = models.ManyToManyField(User, verbose_name='收藏')

    def __str__(self):
        return self.questionTitle


class Comment(models.Model):
    user = models.ForeignKey(User,verbose_name='评论者',on_delete=models.CASCADE)
    question = models.ForeignKey('Question', related_name='comments', on_delete=models.CASCADE)
    commentText = models.TextField(verbose_name='评论内容')
    pubDate = models.DateTimeField(auto_now=True, verbose_name='回答时间')
    goodNum = models.IntegerField(default=0)
    badNum = models.IntegerField(default=0)

    def __str__(self):
        return self.commentText

