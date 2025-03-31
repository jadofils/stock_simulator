from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from .transactionController import TransactionController
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def transaction_list(request):
    transactions = TransactionController.get_all_transactions()
    data = [
        {
            'id': t.id,
            'user_id': t.user.id,
            'stock_id': t.stock.id,
            'transaction_type': t.transaction_type,
            'quantity': str(t.quantity),
            'price_per_share': str(t.price_per_share),
            'total_value': str(t.total_value),
            'timestamp': t.timestamp.isoformat()
        }
        for t in transactions
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
def transaction_detail(request, id):
    transaction = TransactionController.get_transaction_by_id(id)
    if transaction:
        data = {
            'id': transaction.id,
            'user_id': transaction.user.id,
            'stock_id': transaction.stock.id,
            'transaction_type': transaction.transaction_type,
            'quantity': str(transaction.quantity),
            'price_per_share': str(transaction.price_per_share),
            'total_value': str(transaction.total_value),
            'timestamp': transaction.timestamp.isoformat()
        }
        return JsonResponse(data)
    else:
        return HttpResponseNotFound("Transaction not found")

@csrf_exempt
def transaction_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            transaction = TransactionController.create_transaction(
                data['user_id'],
                data['stock_id'],
                data['transaction_type'],
                data['quantity'],
                data['price_per_share']
            )
            if transaction:
                return JsonResponse({
                    'message': 'Transaction created successfully',
                    'transaction': {
                        'id': transaction.id,
                        'user_id': transaction.user.id,
                        'stock_id': transaction.stock.id,
                        'transaction_type': transaction.transaction_type,
                        'quantity': str(transaction.quantity),
                        'price_per_share': str(transaction.price_per_share),
                        'total_value': str(transaction.total_value),
                        'timestamp': transaction.timestamp.isoformat()
                    }
                }, status=201)
            else:
                return JsonResponse({'error': 'Failed to create transaction'}, status=400)
        except (KeyError, json.JSONDecodeError):
            return HttpResponseBadRequest("Invalid data provided")
    else:
        return HttpResponseBadRequest("Only POST requests are allowed")

@csrf_exempt
def transaction_update(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            transaction = TransactionController.update_transaction(
                id,
                data['quantity'],
                data['price_per_share']
            )
            if transaction:
                return JsonResponse({'message': 'Transaction updated successfully'})
            else:
                return HttpResponseNotFound("Transaction not found")
        except (KeyError, json.JSONDecodeError):
            return HttpResponseBadRequest("Invalid data provided")
    else:
        return HttpResponseBadRequest("Only PUT requests are allowed")

@csrf_exempt
def transaction_delete(request, id):
    if request.method == 'DELETE':
        if TransactionController.delete_transaction(id):
            return JsonResponse({'message': 'Transaction deleted successfully'}, status=204)
        else:
            return HttpResponseNotFound("Transaction not found")
    else:
        return HttpResponseBadRequest("Only DELETE requests are allowed")
