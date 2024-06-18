# views.py
from django.shortcuts import render, redirect
from .models import Transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def index(request):
    return render(request, 'finance/accountbook.html')

@csrf_exempt
def add_transaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        date = data['date']
        transaction_type = data['transaction_type']
        amount = data['amount']
        description = data['description']
        transaction = Transaction(date=date, transaction_type=transaction_type, amount=amount, description=description)
        transaction.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

def get_transactions(request):
    transactions = Transaction.objects.all()
    transaction_data = {}

    for transaction in transactions:
        date_str = transaction.date.strftime('%Y-%m-%d')
        if date_str not in transaction_data:
            transaction_data[date_str] = {'income': 0, 'expense': 0}
        if transaction.transaction_type == 'income':
            transaction_data[date_str]['income'] += transaction.amount
        else:
            transaction_data[date_str]['expense'] += transaction.amount

    events = []
    for date, amounts in transaction_data.items():
        income = int(amounts['income'])
        expense = int(amounts['expense'])
        events.append({
            'title': f"+{income} -{expense}",
            'start': date
        })

    return JsonResponse(events, safe=False)

def get_transaction_details(request, date):
    transactions = Transaction.objects.filter(date=date)
    details = []

    for transaction in transactions:
        details.append({
            'id': transaction.id,
            'transaction_type': transaction.transaction_type,
            'amount': int(transaction.amount),
            'description': transaction.description
        })

    return JsonResponse(details, safe=False)

@csrf_exempt
def update_transaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction_id = data['id']
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.amount = data['amount']
        transaction.description = data['description']
        transaction.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

@csrf_exempt
def delete_transaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction_id = data['id']
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})
