from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import TransactionForm
from .models import Transaction
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

def calendar_view(request):
    return render(request, 'accountbookApp/calendar.html')

def get_events(request):
    transactions = Transaction.objects.all()
    events = []
    for transaction in transactions:
        events.append({
            'id': transaction.id,
            'title': f"{transaction.description} ({transaction.amount}₩)",
            'start': transaction.date.isoformat(),
            'backgroundColor': '#00a65a' if transaction.transaction_type == 'income' else '#f56954',
        })
    return JsonResponse(events, safe=False)

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TransactionForm()
    return render(request, 'accountbookApp/add_transaction.html', {'form': form})

def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'accountbookApp/edit_transaction.html', {'form': form, 'transaction': transaction})

def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('/account_book/')
    return render(request, 'accountbookApp/delete_transaction.html', {'transaction': transaction})

def daily_transactions(request):
    today = timezone.now().date()
    transactions = Transaction.objects.filter(date=today)
    return render(request, 'accountbookApp/daily_transactions.html', {'transactions': transactions})

def weekly_transactions(request):
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    transactions = Transaction.objects.filter(date__range=[start_of_week, end_of_week])
    return render(request, 'accountbookApp/weekly_transactions.html', {'transactions': transactions})

def monthly_transactions(request):
    today = timezone.now().date()
    transactions = Transaction.objects.filter(date__year=today.year, date__month=today.month)
    return render(request, 'accountbookApp/monthly_transactions.html', {'transactions': transactions})
