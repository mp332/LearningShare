from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):#在数据库中建立的名为account_userprofil 的数据库表。
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    birth = models.DateField(blank=True, null=True)   # DateField 格式必须为xxxx-xx-xx
    phone = models.CharField(max_length=20, null=True)

'''class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    school = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)'''
