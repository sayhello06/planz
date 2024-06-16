# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('get_transactions/', views.get_transactions, name='get_transactions'),
    path('get_transaction_details/<str:date>/', views.get_transaction_details, name='get_transaction_details'),
    path('update_transaction/', views.update_transaction, name='update_transaction'),
    path('delete_transaction/', views.delete_transaction, name='delete_transaction'),
]
