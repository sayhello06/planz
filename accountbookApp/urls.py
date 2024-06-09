from django.urls import path
from . import views

urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('events/', views.events, name='events'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
]