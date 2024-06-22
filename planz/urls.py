#planz/urls.py
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from planz import settings
from planz.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('calendar/', include('calendarApp.urls')),
    path('', DashboardView.as_view(), name='dashboard'),
    path('accountbook/', include('finance.urls')),
    path('todoList/', include('todoListApp.urls')),
]

