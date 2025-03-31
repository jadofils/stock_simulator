import logging
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

class UserProfileController:
    logger = logging.getLogger(__name__)

    @staticmethod
    def get_all_profiles():
        return UserProfile.objects.all()

    @staticmethod
    def get_profile_by_id(profile_id):
        try:
            return UserProfile.objects.get(id=profile_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_profile(user_id, initial_balance, current_balance, total_investment, total_profit_loss):
        try:
            UserProfileController.logger.info(f"Attempting to fetch user with ID: {user_id}")
            user = User.objects.get(id=user_id)
            UserProfileController.logger.info(f"Creating UserProfile for user {user.username}")
            return UserProfile.objects.create(
                user=user,
                initial_balance=initial_balance,
                current_balance=current_balance,
                total_investment=total_investment,
                total_profit_loss=total_profit_loss
            )
        except User.DoesNotExist:
            UserProfileController.logger.error(f"User with ID {user_id} does not exist")
            return None

    @staticmethod
    def update_profile(profile_id, user_id, initial_balance, current_balance, total_investment, total_profit_loss):
        try:
            user_profile = UserProfile.objects.get(id=profile_id)
            user = User.objects.get(id=user_id)
            user_profile.user = user
            user_profile.initial_balance = initial_balance
            user_profile.current_balance = current_balance
            user_profile.total_investment = total_investment
            user_profile.total_profit_loss = total_profit_loss
            user_profile.save()
            return user_profile
        except (UserProfile.DoesNotExist, User.DoesNotExist):
            return None

    @staticmethod
    def delete_profile(profile_id):
        try:
            user_profile = UserProfile.objects.get(id=profile_id)
            user_profile.delete()
            return True
        except UserProfile.DoesNotExist:
            return False
