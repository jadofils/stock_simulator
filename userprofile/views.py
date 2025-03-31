from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
import logging
from accounts.models import User
from .user_profile_controller import UserProfileController
from django.views.decorators.csrf import csrf_exempt
import json

def user_profile_list(request):
    profiles = UserProfileController.get_all_profiles()
    data = [{'id': p.id, 'user_id': p.user.id, 'initial_balance': str(p.initial_balance), 'current_balance': str(p.current_balance), 'total_investment': str(p.total_investment), 'total_profit_loss': str(p.total_profit_loss)} for p in profiles]
    return JsonResponse(data, safe=False)

def user_profile_detail(request, id):
    profile = UserProfileController.get_profile_by_id(id)
    if profile:
        data = {'id': profile.id, 'user_id': profile.user.id, 'initial_balance': str(profile.initial_balance), 'current_balance': str(profile.current_balance), 'total_investment': str(profile.total_investment), 'total_profit_loss': str(profile.total_profit_loss)}
        return JsonResponse(data)
    else:
        return HttpResponseNotFound("Profile not found")
logger = logging.getLogger(__name__)

@csrf_exempt
def user_profile_create(request, user_id):  # Accept user_id as a parameter
    if request.method == 'POST':
        try:
            logger.info(f"Received POST request to create profile for user_id: {user_id}")
            data = json.loads(request.body)
            logger.info(f"Data received: {data}")

            required_fields = ['initial_balance', 'current_balance', 'total_investment', 'total_profit_loss']
            for field in required_fields:
                if field not in data:
                    logger.error(f"Missing field: {field}")
                    return JsonResponse({'error': f'Missing field: {field}'}, status=400)

            try:
                user = User.objects.get(id=user_id)
                logger.info(f"User found: {user.username}")
            except User.DoesNotExist:
                logger.error(f"User with ID {user_id} does not exist")
                return JsonResponse({'error': 'User with the given ID does not exist'}, status=404)

            profile = UserProfileController.create_profile(
                user.id,
                data['initial_balance'],
                data['current_balance'],
                data['total_investment'],
                data['total_profit_loss']
            )

            if profile:
                logger.info("UserProfile created successfully")
                return JsonResponse({
                    'message': 'UserProfile created successfully',
                    'profile': {
                        'id': profile.id,
                        'user_id': profile.user.id,
                        'initial_balance': str(profile.initial_balance),
                        'current_balance': str(profile.current_balance),
                        'total_investment': str(profile.total_investment),
                        'total_profit_loss': str(profile.total_profit_loss)
                    }
                }, status=201)
            else:
                logger.error("Failed to create UserProfile")
                return JsonResponse({'error': 'Failed to create UserProfile'}, status=500)

        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Invalid JSON or error: {str(e)}")
            return JsonResponse({'error': 'Invalid JSON or missing data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
@csrf_exempt
def user_profile_update(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            profile = UserProfileController.update_profile(
                id,
                data['user_id'],
                data['initial_balance'],
                data['current_balance'],
                data['total_investment'],
                data['total_profit_loss']
            )
            if profile:
                return JsonResponse({'message': 'Profile updated successfully'})
            else:
                return HttpResponseNotFound("Profile not found or invalid user_id")
        except (KeyError, json.JSONDecodeError):
            return HttpResponseBadRequest("Invalid data provided.")
    else:
        return HttpResponseBadRequest("Only PUT requests are allowed.")

@csrf_exempt
def user_profile_delete(request, id):
    if request.method == 'DELETE':
        if UserProfileController.delete_profile(id):
            return HttpResponse(status=204)
        else:
            return HttpResponseNotFound("Profile not found")
    else:
        return HttpResponseBadRequest("Only DELETE requests are allowed.")