from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from .stock_price_history_controller import StockPriceHistoryController
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def stock_price_list(request):
    stock_prices = StockPriceHistoryController.get_all_stock_prices()
    data = [
        {
            'id': sp.id,
            'stock_id': sp.stock.id,
            'open_price': str(sp.open_price),
            'close_price': str(sp.close_price),
            'high_price': str(sp.high_price),
            'low_price': str(sp.low_price),
            'date': sp.date.isoformat()
        }
        for sp in stock_prices
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
def stock_price_detail(request, id):
    stock_price = StockPriceHistoryController.get_stock_price_by_id(id)
    if stock_price:
        data = {
            'id': stock_price.id,
            'stock_id': stock_price.stock.id,
            'open_price': str(stock_price.open_price),
            'close_price': str(stock_price.close_price),
            'high_price': str(stock_price.high_price),
            'low_price': str(stock_price.low_price),
            'date': stock_price.date.isoformat()
        }
        return JsonResponse(data)
    else:
        return HttpResponseNotFound("StockPriceHistory not found")

@csrf_exempt
def stock_price_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stock_price = StockPriceHistoryController.create_stock_price(
                data['stock_id'],
                data['open_price'],
                data['close_price'],
                data['high_price'],
                data['low_price'],
                data['date']
            )
            if stock_price:
                return JsonResponse({
                    'message': 'StockPriceHistory created successfully',
                    'stock_price': {
                        'id': stock_price.id,
                        'stock_id': stock_price.stock.id,
                        'open_price': str(stock_price.open_price),
                        'close_price': str(stock_price.close_price),
                        'high_price': str(stock_price.high_price),
                        'low_price': str(stock_price.low_price),
                        'date': stock_price.date.isoformat()
                    }
                }, status=201)
            else:
                return JsonResponse({'error': 'Failed to create stock price history'}, status=400)
        except (KeyError, json.JSONDecodeError):
            return HttpResponseBadRequest("Invalid data provided")
    else:
        return HttpResponseBadRequest("Only POST requests are allowed")

@csrf_exempt
def stock_price_update(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            stock_price = StockPriceHistoryController.update_stock_price(
                id,
                data['open_price'],
                data['close_price'],
                data['high_price'],
                data['low_price'],
                data['date']
            )
            if stock_price:
                return JsonResponse({'message': 'StockPriceHistory updated successfully'})
            else:
                return HttpResponseNotFound("StockPriceHistory not found")
        except (KeyError, json.JSONDecodeError):
            return HttpResponseBadRequest("Invalid data provided")
    else:
        return HttpResponseBadRequest("Only PUT requests are allowed")

@csrf_exempt
def stock_price_delete(request, id):
    if request.method == 'DELETE':
        if StockPriceHistoryController.delete_stock_price(id):
            return JsonResponse({'message': 'StockPriceHistory deleted successfully'}, status=204)
        else:
            return HttpResponseNotFound("StockPriceHistory not found")
    else:
        return HttpResponseBadRequest("Only DELETE requests are allowed")
