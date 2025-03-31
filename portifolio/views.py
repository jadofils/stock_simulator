from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from .portifolioController import PortfolioController
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def portfolio_list(request):
    portfolios = PortfolioController.get_all_portfolios()
    data = [
        {
            'id': p.id,
            'user_id': p.user.id,
            'stock_id': p.stock.id,
            'quantity': str(p.quantity),
            'purchase_price': str(p.purchase_price),
            'purchase_date': p.purchase_date.isoformat()
        }
        for p in portfolios
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
def portfolio_detail(request, id):
    portfolio = PortfolioController.get_portfolio_by_id(id)
    if portfolio:
        data = {
            'id': portfolio.id,
            'user_id': portfolio.user.id,
            'stock_id': portfolio.stock.id,
            'quantity': str(portfolio.quantity),
            'purchase_price': str(portfolio.purchase_price),
            'purchase_date': portfolio.purchase_date.isoformat()
        }
        return JsonResponse(data)
    else:
        return HttpResponseNotFound("Portfolio not found")

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
                        'purchase_date': portfolio.purchase_date.isoformat()
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
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            portfolio = PortfolioController.update_portfolio(
                id,
                data['quantity'],
                data['purchase_price']
            )
            if portfolio:
                return JsonResponse({'message': 'Portfolio updated successfully'})
            else:
                return HttpResponseNotFound("Portfolio not found")
        except (KeyError, json.JSONDecodeError):
            return HttpResponseBadRequest("Invalid data provided")
    else:
        return HttpResponseBadRequest("Only PUT requests are allowed")

@csrf_exempt
def portfolio_delete(request, id):
    if request.method == 'DELETE':
        if PortfolioController.delete_portfolio(id):
            return HttpResponse(status=204)
        else:
            return HttpResponseNotFound("Portfolio not found")
    else:
        return HttpResponseBadRequest("Only DELETE requests are allowed")
