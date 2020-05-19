from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'answer'

urlpatterns = [
    path('answer/<int:question_id>/', views.answer, name='answer_question'),
    path('answer/like/<int:answer_id>/', views.like, name='like'),
    path('answer/unlike/<int:answer_id>/', views.unlike, name='unlike'),
    path('answer/collect/<int:answer_id>/', views.collect, name='collect'),
    path('answer/change-answer/<int:answer_id>/', views.answer_change, name='answer_change'),
    path('answer/comment/<int:answer_id>/', views.comment, name='answer_comment'),
    path('answer/delete-answer/<int:answer_id>/', views.delete_answer, name='answer_delete'),
    path('answer/show_comment/<int:answer_id>/', views.show_comment, name='show_comment'),
]
