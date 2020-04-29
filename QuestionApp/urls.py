from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import url
from . import views

app_name = 'question'

urlpatterns = [
    # path('index/',views.index,name='index'),
    # path('', RedirectView.as_view(url='index/')),
    path('', views.index, name='index'),
    path('<int:question_id>/', views.question_content, name="question_content"),
    # path('add_question',views.add_question,name='add_question')
    path('add_question/', views.ask, name='add_question'),
    path('search/', views.search, name='search'),

]
