from django.contrib import admin
from .models import Question


@admin.register(Question)  # 注册
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'questionTitle', 'questionCategory', 'questionDescription',
                    'created', 'publishDate')
    list_filter = ['id', 'user', 'questionTitle', 'questionCategory', 'questionDescription',
                   'created', 'publishDate']
# Register your models here.
