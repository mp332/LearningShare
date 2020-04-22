from django.urls import path

from . import views

app_name = 'answer'

urlpatterns = [
    path('answer/', views.answer, name='answer_question'),
]
