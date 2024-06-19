# urls.py
from django.urls import path
from . import views

app_name = "todoListApp"

urlpatterns = [
    path('', views.index, name='index'),
]