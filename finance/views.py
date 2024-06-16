from django.shortcuts import render, redirect
from .models import Transaction
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

def index(request):
    return render(request, 'finance/index.html')

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
