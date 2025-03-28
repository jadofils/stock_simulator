from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password
import json
from accounts.models import User

class AuthController:

    @staticmethod
    def create_user(username, email, password, is_active=True):
        """Create a new user"""
        # Hash the password before saving
        hashed_password = make_password(password)

        # Create the user object
        user = User.objects.create(
            username=username,
            email=email,
            password=hashed_password,
            is_active=is_active
        )

        return user

    @staticmethod
    def get_user(request, user_id):
        """Get a user by ID"""
        try:
            user = get_object_or_404(User, id=user_id)
            return JsonResponse({
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404)

    @staticmethod
    def update_user(user_id, **data):
        """Update a user's details"""
        try:
            user = get_object_or_404(User, id=user_id)

            # Update fields if provided
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            user.save()
            return user
        except Exception as e:
            return str(e)
    @staticmethod
    def delete_user(user_id):
        """Delete a user by ID"""
        try:
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return f"User {user_id} deleted successfully."
        except Exception as e:
            return str(e)

    @staticmethod
    def search_users(request):
        """Search for users by any field (username, email, etc.)"""
        query_params = request.GET
        query = Q()
        
        for field, value in query_params.items():
            if hasattr(User, field):
                query &= Q(**{field: value})

        users = User.objects.filter(query)
        user_list = [
            {"user_id": user.id, "username": user.username, "email": user.email, "is_active": user.is_active}
            for user in users
        ]
        return JsonResponse({"users": user_list}, status=200)

    @staticmethod
    def sort_users(sort_by='id', order='asc'):
        """Sort users by a given field (ascending or descending)"""
        try:
            # If 'desc', prepend '-' to the field name for descending order
            sorted_users = User.objects.all().order_by(sort_by if order == "asc" else f"-{sort_by}")
            
            # Return sorted users
            return sorted_users
        
        except Exception as e:
            # Return error message if any exception occurs
            return JsonResponse({"error": str(e)}, status=400)

    @staticmethod
    def get_all_users(request):
        """Retrieve all users"""
        users = User.objects.all()
        user_list = [
            {"user_id": user.id, "username": user.username, "email": user.email, "is_active": user.is_active}
            for user in users
        ]
        return JsonResponse({"users": user_list}, status=200)
