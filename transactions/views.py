from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import json
from .transactionController import TransactionController

def validate_transaction_data(data, required_fields):
    """Helper function to validate request data"""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {'error': f'Missing required fields: {", ".join(missing_fields)}'}
    return None

@csrf_exempt
def transaction_list(request):
    """Retrieve all transactions with full user and stock details"""
    transactions = TransactionController.get_all_transactions()
    data = [
        {
            'id': t.id,
            'transaction_type': t.transaction_type,
            'quantity': str(t.quantity),
            'price_per_share': str(t.price_per_share),
            'total_value': str(t.total_value),
            'timestamp': t.timestamp.isoformat(),
            'user': {
                'id': t.user.id,
                'username': f"{t.user.username} ",
                'email': t.user.email
            },
            'stock': {
                'id': t.stock.id,
                'name': t.stock.name,
                'symbol': t.stock.symbol,
                'current_price': str(t.stock.current_price),
                'market_cap': str(t.stock.market_cap)
            }
        }
        for t in transactions
    ]
    return JsonResponse({"transactions": data}, safe=False, status=200)

@csrf_exempt
def transaction_detail(request, id):
    """Retrieve a specific transaction with full user and stock details"""
    transaction = TransactionController.get_transaction_by_id(id)
    if transaction:
        data = {
            'id': transaction.id,
            'transaction_type': transaction.transaction_type,
            'quantity': str(transaction.quantity),
            'price_per_share': str(transaction.price_per_share),
            'total_value': str(transaction.total_value),
            'timestamp': transaction.timestamp.isoformat(),
            'user': {
                'id': transaction.user.id,
                'username': f"{transaction.user.username} ",
                'email': transaction.user.email
            },
            'stock': {
                'id': transaction.stock.id,
                'name': transaction.stock.name,
                'symbol': transaction.stock.symbol,
                'current_price': str(transaction.stock.current_price),
                'market_cap': str(transaction.stock.market_cap)
            }
        }
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({'error': 'Transaction not found'}, status=404)

@csrf_exempt
def transaction_create(request):
    """Create a new transaction"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            validation_error = validate_transaction_data(data, ['user_id', 'stock_id', 'transaction_type', 'quantity', 'price_per_share'])
            if validation_error:
                return JsonResponse(validation_error, status=400)

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
                        'transaction_type': transaction.transaction_type,
                        'quantity': str(transaction.quantity),
                        'price_per_share': str(transaction.price_per_share),
                        'total_value': str(transaction.total_value),
                        'timestamp': transaction.timestamp.isoformat(),
                        'user': {
                            'id': transaction.user.id,
                            'username': f"{transaction.user.username} ",
                            'email': transaction.user.email
                        },
                        'stock': {
                            'id': transaction.stock.id,
                            'name': transaction.stock.name,
                            'symbol': transaction.stock.symbol,
                            'current_price': str(transaction.stock.current_price),
                            'market_cap': str(transaction.stock.market_cap)
                        }
                    }
                }, status=201)
            else:
                return JsonResponse({'error': 'Failed to create transaction'}, status=400)
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid JSON data provided'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
# NOT NECESSARY TO UPDATE THE TRANSACTION MADE
# @csrf_exempt
# def transaction_update(request, id):
#     """Update a transaction"""
#     if request.method == 'PUT':
#         try:
#             data = json.loads(request.body)
#             validation_error = validate_transaction_data(data, ['quantity', 'price_per_share'])
#             if validation_error:
#                 return JsonResponse(validation_error, status=400)

#             transaction = TransactionController.update_transaction(
#                 id,
#                 data['quantity'],
#                 data['price_per_share']
#             )
#             if transaction:
#                 return JsonResponse({'message': 'Transaction updated successfully'}, status=200)
#             else:
#                 return JsonResponse({'error': 'Transaction not found'}, status=404)
#         except (json.JSONDecodeError, KeyError):
#             return JsonResponse({'error': 'Invalid JSON data provided'}, status=400)
#     else:
#         return JsonResponse({'error': 'Only PUT requests are allowed'}, status=405)

@csrf_exempt
def transaction_delete(request, id):
    """Delete a transaction"""
    if request.method == 'DELETE':
        if TransactionController.delete_transaction(id):
            return JsonResponse({'message': 'Transaction deleted successfully'}, status=204)
        else:
            return JsonResponse({'error': 'Transaction not found'}, status=404)
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)
