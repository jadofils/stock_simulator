from accounts.models import Stock, StockPriceHistory
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

class StockPriceHistoryController:
    @staticmethod
    def get_all_stock_prices():
        return StockPriceHistory.objects.all()

    @staticmethod
    def get_stock_price_by_id(stock_price_id):
        try:
            return StockPriceHistory.objects.get(id=stock_price_id)
        except ObjectDoesNotExist:
            logger.error(f"StockPriceHistory with ID {stock_price_id} does not exist")
            return None

    @staticmethod
    def create_stock_price(stock_id, open_price, close_price, high_price, low_price, date):
        try:
            stock = Stock.objects.get(id=stock_id)
            stock_price = StockPriceHistory.objects.create(
                stock=stock,
                open_price=open_price,
                close_price=close_price,
                high_price=high_price,
                low_price=low_price,
                date=date
            )
            logger.info("StockPriceHistory created successfully")
            return stock_price
        except Stock.DoesNotExist:
            logger.error(f"Stock with ID {stock_id} does not exist")
            return None

    @staticmethod
    def update_stock_price(stock_price_id, open_price, close_price, high_price, low_price, date):
        try:
            stock_price = StockPriceHistory.objects.get(id=stock_price_id)
            stock_price.open_price = open_price
            stock_price.close_price = close_price
            stock_price.high_price = high_price
            stock_price.low_price = low_price
            stock_price.date = date
            stock_price.save()
            logger.info(f"StockPriceHistory with ID {stock_price_id} updated successfully")
            return stock_price
        except StockPriceHistory.DoesNotExist:
            logger.error(f"StockPriceHistory with ID {stock_price_id} does not exist")
            return None

    @staticmethod
    def delete_stock_price(stock_price_id):
        try:
            stock_price = StockPriceHistory.objects.get(id=stock_price_id)
            stock_price.delete()
            logger.info(f"StockPriceHistory with ID {stock_price_id} deleted successfully")
            return True
        except StockPriceHistory.DoesNotExist:
            logger.error(f"StockPriceHistory with ID {stock_price_id} does not exist")
            return False
