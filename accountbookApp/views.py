# accountbookApp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import Transaction
from .forms import TransactionForm
import json

class CalendarView(TemplateView):
    template_name = 'accountbookApp/calendar.html'

def events(request):
    transactions = Transaction.objects.all()
    events = []
    for transaction in transactions:
        events.append({
            'id': transaction.id,
            'title': f"{transaction.title} ({'+' if transaction.transaction_type == 'income' else '-' }₩{transaction.amount})",
            'start': transaction.date.strftime('%Y-%m-%d'),
            'allDay': True,
            'color': 'green' if transaction.transaction_type == 'income' else 'red',
        })
    return JsonResponse(events, safe=False)

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'errors': form.errors})
    else:
        form = TransactionForm()
    return render(request, 'accountbookApp/add_transaction.html', {'form': form})

def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'accountbookApp/edit_transaction.html', {'form': form, 'transaction': transaction})

def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('calendar')
    return render(request, 'accountbookApp/delete_transaction.html', {'transaction': transaction})
