from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from .stock_price_history_controller import StockPriceHistoryController
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.http import JsonResponse

@csrf_exempt
def stock_price_list(request):
    # Validate the request method
    if request.method != 'GET':
        return HttpResponseBadRequest("Only GET requests are allowed")

    try:
        # Fetch all stock price data
        stock_prices = StockPriceHistoryController.get_all_stock_prices()

        # Check if stock prices exist
        if not stock_prices:
            return JsonResponse({"message": "No stock price data found"}, status=404)

        # Prepare the JSON response data
        data = [
            {
                'id': sp.id,
                'stock_id': sp.stock.id,
                'open_price': str(sp.open_price),
                'close_price': str(sp.close_price),
                'high_price': str(sp.high_price),
                'low_price': str(sp.low_price),
                'date': sp.date.isoformat(),
                'stock': {
                    'id': sp.stock.id,
                    'name': sp.stock.name,
                    'symbol': sp.stock.symbol,
                    'current_price': sp.stock.current_price,
                    'market_cap': sp.stock.market_cap,
                    'last_updated': sp.stock.last_updated.isoformat()
                }
            }
            for sp in stock_prices
        ]

        # Return the JSON response
        return JsonResponse({"data": data}, safe=False, status=200)

    except Exception as e:
        # Handle unexpected errors
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

@csrf_exempt
def stock_price_detail(request, id):
    # Validate the request method
    if request.method != 'GET':
        return HttpResponseBadRequest("Only GET requests are allowed")

    try:
        # Attempt to fetch the stock price by ID
        stock_price = StockPriceHistoryController.get_stock_price_by_id(id)

        if stock_price:
            # Prepare the response data
            data = {
                'id': stock_price.id,
                'stock_id': stock_price.stock.id,
                'open_price': str(stock_price.open_price),
                'close_price': str(stock_price.close_price),
                'high_price': str(stock_price.high_price),
                'low_price': str(stock_price.low_price),
                'date': stock_price.date.isoformat()
            }
            return JsonResponse({"data": data}, status=200)
        else:
            return JsonResponse({"message": "Stock price not found"}, status=404)

    except Exception as e:
        # Handle unexpected errors
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)



@csrf_exempt
def stock_price_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Convert date from string to datetime object
            if isinstance(data.get('date'), str):
                try:
                    data['date'] = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DDTHH:MM:SS'}, status=400)

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
                    },
                    'stock': {
                        'id': stock_price.stock.id,
                        'name': stock_price.stock.name,
                        'symbol': stock_price.stock.symbol,
                        'current_price': stock_price.stock.current_price,
                        'market_cap': stock_price.stock.market_cap,
                        'last_updated': stock_price.stock.last_updated.isoformat()
                    }
                }, status=201)

            return JsonResponse({'error': 'Failed to create stock price history'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)

        except Exception as e:
            return JsonResponse({'error': f'Internal Server Error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)



@csrf_exempt
def stock_price_update(request, id):
    if request.method != 'PUT':
        return HttpResponseBadRequest("Only PUT requests are allowed")

    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['open_price', 'close_price', 'high_price', 'low_price', 'date']
        for field in required_fields:
            if field not in data:
                return HttpResponseBadRequest(f"Missing required field: {field}")

        # Attempt to update the stock price
        stock_price = StockPriceHistoryController.update_stock_price(
            id,
            data['open_price'],
            data['close_price'],
            data['high_price'],
            data['low_price'],
            data['date']
        )

        if stock_price:
            # Prepare the response data
            return JsonResponse({
                'message': 'StockPriceHistory updated successfully',
                'stock': {
                    'id': stock_price.stock.id,
                    'name': stock_price.stock.name,
                    'symbol': stock_price.stock.symbol,
                    "current_price": str(stock_price.stock.current_price),
                    'market_cap': str(stock_price.stock.market_cap),
                    'last_updated': stock_price.stock.last_updated.isoformat()
                }
            }, status=200)
        else:
            return HttpResponseNotFound("StockPriceHistory not found")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON data provided")
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
    
@csrf_exempt
def stock_price_delete(request, id):
    if request.method != 'DELETE':
        return HttpResponseBadRequest("Only DELETE requests are allowed")

    try:
        # Attempt to delete the stock price
        deleted = StockPriceHistoryController.delete_stock_price(id)

        if deleted:
            return JsonResponse({'message': 'StockPriceHistory deleted successfully'}, status=204)  # No content
        else:
            return JsonResponse({'message': 'StockPriceHistory not found'}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
