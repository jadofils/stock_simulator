from accounts.models import User, Stock, Transaction
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

class TransactionController:
    @staticmethod
    def get_all_transactions():
        return Transaction.objects.all()

    @staticmethod
    def get_transaction_by_id(transaction_id):
        try:
            return Transaction.objects.get(id=transaction_id)
        except ObjectDoesNotExist:
            logger.error(f"Transaction with ID {transaction_id} does not exist")
            return None

    @staticmethod
    def create_transaction(user_id, stock_id, transaction_type, quantity, price_per_share):
        try:
            user = User.objects.get(id=user_id)
            stock = Stock.objects.get(id=stock_id)
            total_value = quantity * price_per_share
            transaction = Transaction.objects.create(
                user=user,
                stock=stock,
                transaction_type=transaction_type,
                quantity=quantity,
                price_per_share=price_per_share,
                total_value=total_value
            )
            logger.info("Transaction created successfully")
            return transaction
        except (User.DoesNotExist, Stock.DoesNotExist) as e:
            logger.error(f"Error while creating transaction: {str(e)}")
            return None

#NO transaction updates on the dataase after sell or buy
    # @staticmethod
    # def update_transaction(transaction_id, quantity, price_per_share):
    #     try:
    #         transaction = Transaction.objects.get(id=transaction_id)
    #         transaction.quantity = quantity
    #         transaction.price_per_share = price_per_share
    #         transaction.total_value = quantity * price_per_share
    #         transaction.save()
    #         logger.info(f"Transaction with ID {transaction_id} updated successfully")
    #         return transaction
    #     except Transaction.DoesNotExist:
    #         logger.error(f"Transaction with ID {transaction_id} does not exist")
    #         return None

    @staticmethod
    def delete_transaction(transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            transaction.delete()
            logger.info(f"Transaction with ID {transaction_id} deleted successfully")
            return True
        except Transaction.DoesNotExist:
            logger.error(f"Transaction with ID {transaction_id} does not exist")
            return False
