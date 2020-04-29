from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'answer'

urlpatterns = [
    path('answer/<int:question_id>/', views.answer, name='answer_question'),
]
