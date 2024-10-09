#mindmap/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_keyword/', views.add_keyword, name='add_keyword'),
    path('load_map/<str:keyword>/', views.load_map, name='load_map'),
]
