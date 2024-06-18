from django.shortcuts import render
from calendarApp.models import Event
from finance.models import Transaction
from django.views.generic import View

class DashboardView(View):
    def get(self, request):
        return render(request, 'index.html')