#mindmap/urls.py

from django.urls import path
from .views import index, save_project, list_projects, project_detail, recommend_topics_page, recommend_topics

urlpatterns = [
    path('', index, name='index'),
    path('recommend_topics/', recommend_topics_page, name='recommend_topics_page'),
    path('recommendation/', recommend_topics, name='recommend_topics'),
    path('save_project/', save_project, name='save_project'),
    path('list_projects/', list_projects, name='list_projects'),
    path('project/<int:project_id>/', project_detail, name='project_detail'),
]
