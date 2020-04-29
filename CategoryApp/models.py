from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    分组模块
    """
    name = models.CharField(max_length=20, unique=True, verbose_name='分组名称')
    number = models.IntegerField(unique=True, verbose_name='分组序号')

    def __str__(self):
        return self.name
