from django.contrib import admin
from .models import AnswerModel


@admin.register(AnswerModel)    # 注册
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'question', 'pub_date')
    list_filter = ['id', 'author', 'question', 'pub_date']

# Register your models here.
