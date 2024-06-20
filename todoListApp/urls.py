from django.urls import path
from . import views

app_name = "todoListApp"

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_todo, name='add_todo'),
    path('done/<int:todo_id>/', views.mark_done, name='mark_done'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]
