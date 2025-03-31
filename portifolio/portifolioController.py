from accounts.models import Stock,Portfolio,User

from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

class PortfolioController:
    @staticmethod
    def get_all_portfolios():
        return Portfolio.objects.all()

    @staticmethod
    def get_portfolio_by_id(portfolio_id):
        try:
            return Portfolio.objects.get(id=portfolio_id)
        except ObjectDoesNotExist:
            logger.error(f"Portfolio with ID {portfolio_id} does not exist")
            return None

    @staticmethod
    def create_portfolio(user_id, stock_id, quantity, purchase_price):
        try:
            user = User.objects.get(id=user_id)
            stock = Stock.objects.get(id=stock_id)
            portfolio = Portfolio.objects.create(
                user=user,
                stock=stock,
                quantity=quantity,
                purchase_price=purchase_price
            )
            logger.info("Portfolio created successfully")
            return portfolio
        except (User.DoesNotExist, Stock.DoesNotExist) as e:
            logger.error(f"Error while creating portfolio: {str(e)}")
            return None

    @staticmethod
    def update_portfolio(portfolio_id, quantity, purchase_price):
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
            portfolio.quantity = quantity
            portfolio.purchase_price = purchase_price
            portfolio.save()
            logger.info(f"Portfolio with ID {portfolio_id} updated successfully")
            return portfolio
        except Portfolio.DoesNotExist:
            logger.error(f"Portfolio with ID {portfolio_id} does not exist")
            return None

    @staticmethod
    def delete_portfolio(portfolio_id):
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
            portfolio.delete()
            logger.info(f"Portfolio with ID {portfolio_id} deleted successfully")
            return True
        except Portfolio.DoesNotExist:
            logger.error(f"Portfolio with ID {portfolio_id} does not exist")
            return False
