from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
]
