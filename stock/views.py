
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .stockController import StockController

@csrf_exempt
def create_stock(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            stock = StockController.create_stock(**data)
            return JsonResponse({
                'id': stock.id,
                'symbol': stock.symbol,
                'name': stock.name,
                'current_price': str(stock.current_price),
                'previous_close': str(stock.previous_close),
                'market_cap': str(stock.market_cap),
                'last_updated': stock.last_updated,
            }, status=201)
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_stock(request, stock_id):
    stock = StockController.get_stock(stock_id)
    if stock:
        return JsonResponse({
            'id': stock.id,
            'symbol': stock.symbol,
            'name': stock.name,
            'current_price': str(stock.current_price),
            'previous_close': str(stock.previous_close),
            'market_cap': str(stock.market_cap),
            'last_updated': stock.last_updated,
        })
    return JsonResponse({'error': 'Stock not found'}, status=404)

@csrf_exempt
def update_stock(request, stock_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            stock = StockController.update_stock(stock_id, **data)
            if stock:
                return JsonResponse({
                    'id': stock.id,
                    'symbol': stock.symbol,
                    'name': stock.name,
                    'current_price': str(stock.current_price),
                    'previous_close': str(stock.previous_close),
                    'market_cap': str(stock.market_cap),
                    'last_updated': stock.last_updated,
                })
            return JsonResponse({'error': 'Stock not found'}, status=404)
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_stock(request, stock_id):
    if request.method == 'DELETE':
        if StockController.delete_stock(stock_id):
            return JsonResponse({'message': 'Stock deleted successfully'})
        return JsonResponse({'error': 'Stock not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_all_stocks(request):
    stocks = StockController.get_all_stocks()
    stock_list = [{
        'id': stock.id,
        'symbol': stock.symbol,
        'name': stock.name,
        'current_price': str(stock.current_price),
        'previous_close': str(stock.previous_close),
        'market_cap': str(stock.market_cap),
        'last_updated': stock.last_updated,
    } for stock in stocks]
    return JsonResponse({'stocks': stock_list})

