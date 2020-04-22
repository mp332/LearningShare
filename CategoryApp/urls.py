from django.conf.urls import url
from . import views

app_name = 'CategoryApp'

urlpatterns = [
    url(r'', views.category, name="category"),
]
