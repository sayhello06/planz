#mindmap/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recommend_topics/', views.recommend_topics_page, name='recommend_topics_page'),
    path('recommendation/', views.recommend_topics, name='recommend_topics'),
    path('save_project/', views.save_project, name='save_project'),
    path('list_projects/', views.list_projects, name='list_projects'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('delete_project/', views.delete_project, name='delete_project'),
]
