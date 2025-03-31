from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
import logging
from accounts.models import User, UserProfile
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
        user = profile.user  # Get the associated User object
        data = {
            'profile': {
                'id': profile.id,
                'user_id': profile.user.id,
                'initial_balance': str(profile.initial_balance),
                'current_balance': str(profile.current_balance),
                'total_investment': str(profile.total_investment),
                'total_profit_loss': str(profile.total_profit_loss),
            },
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'date_joined': user.date_joined.isoformat(),  # Convert datetime to ISO format
            }
        }
        return JsonResponse(data)
    else:
      return JsonResponse({'error': 'Profile not found'}, status=404)

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

            # Check if a UserProfile already exists for the given user_id
            if UserProfile.objects.filter(user=user).exists():
                logger.error(f"UserProfile already exists for user_id: {user_id}")
                return JsonResponse({'error': 'UserProfile already exists for this user'}, status=409)  # 409 Conflict

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
                        'total_profit_loss': str(profile.total_profit_loss),
                    },
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'is_active': user.is_active,
                        'date_joined': user.date_joined.isoformat(),  # Convert datetime to ISO format
                        # Add any other user fields you want to include
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
def user_profile_update(request, id, user_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)

            # Validate user_id from the URL
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            # Validate profile exists and belongs to the user
            try:
                profile = UserProfile.objects.get(id=id, user=user)
            except UserProfile.DoesNotExist:
                return JsonResponse({'error': 'Profile not found or does not belong to user'}, status=404)

            # Update the profile using the controller
            profile = UserProfileController.update_profile(
                id,
                user_id,
                data['initial_balance'],
                data['current_balance'],
                data['total_investment'],
                data['total_profit_loss']
            )

            if profile:
                return JsonResponse({
                    'message': 'Profile updated successfully',
                    'profile': {
                        'id': profile.id,
                        'user_id': profile.user.id,
                        'initial_balance': str(profile.initial_balance),
                        'current_balance': str(profile.current_balance),
                        'total_investment': str(profile.total_investment),
                        'total_profit_loss': str(profile.total_profit_loss),
                    },
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'is_active': user.is_active,
                        'date_joined': user.date_joined.isoformat(),
                    }
                })
            else:
                return JsonResponse({'error': 'Failed to update profile'}, status=500)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid JSON or missing data'}, status=400)
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'}, status=405)


@csrf_exempt
def user_profile_delete(request, id, user_id):
    if request.method == 'DELETE':
        try:
            # Validate that the user exists
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            # Validate that the profile exists and is linked to the user
            try:
                profile = UserProfile.objects.get(id=id, user=user)
            except UserProfile.DoesNotExist:
                return JsonResponse({'error': 'Profile not found or does not belong to the user'}, status=404)

            # Perform the deletion
            if UserProfileController.delete_profile(id):
                return JsonResponse({'message': 'Profile deleted successfully'}, status=204)
            else:
                return JsonResponse({'error': 'Failed to delete profile'}, status=500)

        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)
