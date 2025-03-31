import logging
from venv import logger
from accounts.models import User
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
            print('user id',user_id)
            user = User.objects.get(id=user_id)
            print("user from objects db:",user)
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
            logger.info(f"Attempting to fetch UserProfile with ID: {profile_id}")
            user_profile = UserProfile.objects.get(id=profile_id)

            logger.info(f"Attempting to fetch User with ID: {user_id}")
            user = User.objects.get(id=user_id)

            # Updating the profile fields
            user_profile.user = user
            user_profile.initial_balance = initial_balance
            user_profile.current_balance = current_balance
            user_profile.total_investment = total_investment
            user_profile.total_profit_loss = total_profit_loss
            user_profile.save()

            logger.info(f"UserProfile with ID {profile_id} updated successfully")
            return user_profile
        except UserProfile.DoesNotExist:
            logger.error(f"UserProfile with ID {profile_id} does not exist")
            return None
        except User.DoesNotExist:
            logger.error(f"User with ID {user_id} does not exist")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None

    @staticmethod
    def delete_profile(profile_id):
        try:
            logger.info(f"Attempting to delete UserProfile with ID: {profile_id}")
            user_profile = UserProfile.objects.get(id=profile_id)
            user_profile.delete()
            logger.info(f"UserProfile with ID {profile_id} deleted successfully")
            return True
        except UserProfile.DoesNotExist:
            logger.error(f"UserProfile with ID {profile_id} does not exist")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred while deleting: {e}")
            return False