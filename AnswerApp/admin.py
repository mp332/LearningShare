from django.contrib import admin
from .models import Answer


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'pub_date')
    list_filter = ['id', 'user', 'question', 'pub_date']


admin.site.register(Answer, AnswerAdmin)
# Register your models here.
