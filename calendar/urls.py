from django.urls import path
from .views import calendar, add_event, update_event, delete_event

#app_name = "calendar"

urlpatterns = [
    path('', calendar, name='calendar'),
    path('add_event/', add_event, name='add_event'),
    path('update_event/<int:event_id>/', update_event, name='update_event'),
    path('delete_event/<int:event_id>/', delete_event, name='delete_event'),
]
