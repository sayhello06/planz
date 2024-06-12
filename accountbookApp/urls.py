from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('events/', views.get_events, name='get_events'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('daily/', views.daily_transactions, name='daily_transactions'),
    path('weekly/', views.weekly_transactions, name='weekly_transactions'),
    path('monthly/', views.monthly_transactions, name='monthly_transactions'),
]
