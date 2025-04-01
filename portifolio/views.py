from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from .portifolioController import PortfolioController
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def portfolio_list(request):
    # Validate the request method
    if request.method != 'GET':
        return JsonResponse({"error": "Invalid request method. Only GET is allowed."}, status=405)

    try:
        # Fetch all portfolios from the controller
        portfolios = PortfolioController.get_all_portfolios()
        
        if not portfolios:
            return JsonResponse({"error": "No portfolios found."}, status=404)
        
        # Prepare the response data
        data = [
            {
                'id': p.id,
                'user_id': p.user.id,
                'stock_id': p.stock.id,
                'quantity': str(p.quantity),
                'purchase_price': str(p.purchase_price),
                'purchase_date': p.purchase_date.isoformat(),
                'user': {
                    'id': p.user.id,
                    'name': p.user.username,
                    'email': p.user.email
                },
                'stock': {
                    'id': p.stock.id,
                    'name': p.stock.name,
                    'symbol': p.stock.symbol,
                    'price': p.stock.current_price,
                    'previous_close': p.stock.previous_close,
                    'market_cap': p.stock.market_cap
                }
            }
            for p in portfolios
        ]
        
        # Return the JSON response
        return JsonResponse({"data": data}, safe=False, status=200)

    except Exception as e:
        # Handle unexpected errors
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)



@csrf_exempt
def portfolio_detail(request, id):
    # Validate the request method
    if request.method != 'GET':
        return JsonResponse({"error": "Invalid request method. Only GET is allowed."}, status=405)
    
    # Attempt to fetch portfolio details
    try:
        portfolio = PortfolioController.get_portfolio_by_id(id)
        if not portfolio:
            return JsonResponse({"error": "Portfolio not found."}, status=404)
        
        # Prepare the response data
        data = {
            'portfolio': {
                'id': portfolio.id,
                'user_id': portfolio.user.id,
                'stock_id': portfolio.stock.id,
                'quantity': str(portfolio.quantity),
                'purchase_price': str(portfolio.purchase_price),
                'purchase_date': portfolio.purchase_date.isoformat(),
                'user': {
                    'id': portfolio.user.id,
                    'name': portfolio.user.username,
                    'email': portfolio.user.email
                },
                'stock': {
                    'id': portfolio.stock.id,
                    'name': portfolio.stock.name,
                    'symbol': portfolio.stock.symbol,
                    'price': portfolio.stock.current_price,
                    'previous_close': portfolio.stock.previous_close,
                    'market_cap': portfolio.stock.market_cap
                }
            }
        }

        # Return successful JSON response
        return JsonResponse({"data": data}, status=200)

    except Exception as e:
        # Handle any unexpected errors
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

@csrf_exempt
def portfolio_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            portfolio = PortfolioController.create_portfolio(
                data['user_id'],
                data['stock_id'],
                data['quantity'],
                data['purchase_price']
            )
            if portfolio:
                return JsonResponse({
                    'message': 'Portfolio created successfully',
                    'portfolio': {
                        'id': portfolio.id,
                        'user_id': portfolio.user.id,
                        'stock_id': portfolio.stock.id,
                        'quantity': str(portfolio.quantity),
                        'purchase_price': str(portfolio.purchase_price),
                        'purchase_date': portfolio.purchase_date.isoformat() ,
                'user': {
                    'id': portfolio.user.id,
                    'name': portfolio.user.username,
                    'email': portfolio.user.email,
                    "stock":{
                        "id":portfolio.stock.id,
                        "name": portfolio.stock.name,
                        "symbol":portfolio.stock.symbol,
                        "price": portfolio.stock.current_price,
                        "previous_close": portfolio.stock.previous_close,
                        "market_cap": portfolio.stock.market_cap,
                    }
                }
                    }
                }, status=201)
            else:
                return JsonResponse({'error': 'Failed to create portfolio'}, status=400)
        except (KeyError, json.JSONDecodeError):
            return HttpResponseBadRequest("Invalid data provided")
    else:
        return HttpResponseBadRequest("Only POST requests are allowed")

@csrf_exempt
def portfolio_update(request, id):
    if request.method != 'PUT':
        return HttpResponseBadRequest("Only PUT requests are allowed")
    
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body)
        
        # Validate required fields
        if 'quantity' not in data or 'purchase_price' not in data:
            return HttpResponseBadRequest("Missing required fields: 'quantity' and 'purchase_price'")
        
        # Attempt to update the portfolio
        portfolio = PortfolioController.update_portfolio(
            id,
            data['quantity'],
            data['purchase_price']
        )
        
        if portfolio:
            return JsonResponse({
                'message': 'Portfolio updated successfully',
                'portfolio': {
                    'id': portfolio.id,
                    'quantity': str(portfolio.quantity),
                    'purchase_price': str(portfolio.purchase_price)
                }
            }, status=200)
        else:
            return HttpResponseNotFound("Portfolio not found")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON data provided")
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

@csrf_exempt
def portfolio_delete(request, id):
    if request.method != 'DELETE':
        return HttpResponseBadRequest("Only DELETE requests are allowed")
    
    try:
        # Attempt to delete the portfolio
        deleted = PortfolioController.delete_portfolio(id)
        
        if deleted:
            return HttpResponse(status=204)  # No Content response
        else:
            # Correct key-value pair for the response
            return JsonResponse({"message": "Portfolio not found"}, status=404)
    except Exception as e:
        # Proper JsonResponse with `safe=False` for error handling, if needed
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)