from django.shortcuts import render, redirect
from django.utils.timezone import now
from calendarApp.models import Event
from finance.models import Transaction
from datetime import datetime, timedelta
from django.views import View
from todoListApp.models import Todo
import pytz

class DashboardView(View):
    def get(self, request):
        seoul_tz = pytz.timezone('Asia/Seoul')
        current_date = datetime.now(seoul_tz).date()
        
        # Get upcoming events
        upcoming_events = Event.objects.filter(start__gte=current_date).order_by('start')[:4]
        event_data = []
        for event in upcoming_events:
            days_left = (event.start.date() - current_date).days
            event_data.append({
                'title': event.title,
                'days_left': days_left
            })

        # Get daily and monthly transactions
        daily_transactions = Transaction.objects.filter(date=current_date)
        monthly_transactions = Transaction.objects.filter(date__year=current_date.year, date__month=current_date.month)

        def get_transaction_summary(transactions):
            income = sum(t.amount for t in transactions if t.transaction_type == 'income')
            expense = sum(t.amount for t in transactions if t.transaction_type == 'expense')
            return {
                'income': income,
                'expense': expense
            }

        daily_summary = get_transaction_summary(daily_transactions)
        monthly_summary = get_transaction_summary(monthly_transactions)
        todos = Todo.objects.filter(is_done=False)
        done_todos = Todo.objects.filter(is_done=True)

        context = {
            'events': event_data,
            'daily_summary': daily_summary,
            'monthly_summary': monthly_summary,
            'todos': todos,
            'done_todos': done_todos
        }

        return render(request, 'index.html', context)
    
    def mark_done(request, todo_id):
        todo = Todo.objects.get(id=todo_id)
        todo.is_done = True
        todo.save()
        return redirect('dashboard')

    def delete_todo(request, todo_id):
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return redirect('dashboard')