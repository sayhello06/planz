from django.urls import path
from .views import calendar
from calendarApp import views

#app_name = "calendarApp"

urlpatterns = [
    path('', views.calendar, name='calendar'),
    path('all_events/', views.all_events, name='all_events'),
    path('add_event/', views.add_event, name='add_event'),
    path('update_event/', views.update_event, name='update_event'),
    path('remove_event/', views.remove_event, name='remove_event'),
]
