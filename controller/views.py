from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from accounts.models import User
from .controller import AuthController  # Ensure you import the AuthController

from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt  # Temporarily disable CSRF protection for API
def create_user(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            is_active = data.get('is_active', True)  # Default to True if not provided
            print("data", data)

            if not username or not email or not password:
                return JsonResponse({'error': 'Username, email, and password are required'}, status=400)

            # Hash the password before saving
            hashed_password = make_password(password)

            # Call the create_user method from AuthController to create the user
            user = AuthController.create_user(username=username, email=email, password=hashed_password, is_active=is_active)
            
            return JsonResponse({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'date_joined': user.date_joined,
            }
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
@csrf_exempt
def get_all_users(request):
    try:
        # Get all users from the User model
        users = User.objects.all()
        
        # Prepare the data to return in the response
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'date_joined': user.date_joined,
            })
        
        return JsonResponse({'users': users_data})
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'No users found'}, status=404)
@csrf_exempt    
def search_users(request):
    # Search logic based on query parameters (example)
    username = request.GET.get('username', '')
    email = request.GET.get('email', '')

    users = User.objects.filter(username__icontains=username, email__icontains=email)

    user_data = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
        }
        for user in users
    ]

    return JsonResponse({'users': user_data})
@csrf_exempt
def update_user(request, user_id):
    if request.method == 'PUT':
        try:
            # Parse request body as JSON
            data = json.loads(request.body.decode('utf-8'))

            # Call static method to update the user
            updated_user = AuthController.update_user(user_id=user_id, **data)

            if isinstance(updated_user, User):
                return JsonResponse({
                    'message': 'User updated successfully',
                    'user': {
                        'id': updated_user.id,
                        'username': updated_user.username,
                        'email': updated_user.email,
                        'is_active': updated_user.is_active,
                        'date_joined': updated_user.date_joined
                    }
                }, status=200)
            else:
                # If the returned value is an error message, return it
                return JsonResponse({'error': updated_user}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            # Call delete_user method from AuthController
            message = AuthController.delete_user(user_id=user_id)
            return JsonResponse({'message': message}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=404)

@csrf_exempt
def sort_users(request, sort_by, order):
    try:
        # Validate the 'order' parameter to ensure it's either 'asc' or 'desc'
        if order not in ['asc', 'desc']:
            return JsonResponse({"error": "Order must be 'asc' or 'desc'."}, status=400)

        # Check if the field to sort by is valid
        valid_sort_fields = ['id', 'username', 'email', 'date_joined', 'is_active']
        if sort_by not in valid_sort_fields:
            return JsonResponse({"error": f"Invalid sort field. Valid options are: {', '.join(valid_sort_fields)}."}, status=400)

        # Perform the sorting based on the parameters
        sorted_users = User.objects.all().order_by(sort_by if order == "asc" else f"-{sort_by}")
        
        # Prepare the data to send in response
        user_list = [
            {"id": user.id, "username": user.username, "email": user.email, "is_active": user.is_active, "date_joined": user.date_joined}
            for user in sorted_users
        ]

        # Return the sorted list as a JSON response
        return JsonResponse({"users": user_list}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)







from django.http import JsonResponse
from django.contrib.auth import authenticate




@csrf_exempt  # Temporarily disable CSRF protection for API
def login(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Email and password are required'}, status=400)

            try:
                # Fetch the user by email
                user = User.objects.get(email=email)

                # Authenticate the user using username (since authenticate uses username, not email)
                user = authenticate(request, username=user.username, password=password)

                if user is not None and user.is_active:
                    return JsonResponse({'message': 'Login successful', 'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'is_active': user.is_active,
                        'date_joined': user.date_joined
                    }})
                else:
                    return JsonResponse({'error': 'Invalid credentials or account inactive'}, status=401)

            except User.DoesNotExist:
                return JsonResponse({'error': 'User with this email does not exist'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)