from accounts.models import Stock

class StockController:
    @staticmethod
    def create_stock(symbol, name, current_price, previous_close, market_cap):
        stock = Stock.objects.create(
            symbol=symbol,
            name=name,
            current_price=current_price,
            previous_close=previous_close,
            market_cap=market_cap,
        )
        return stock

    @staticmethod
    def get_stock(stock_id):
        try:
            stock = Stock.objects.get(id=stock_id)
            return stock
        except Stock.DoesNotExist:
            return None

    @staticmethod
    def update_stock(stock_id, symbol=None, name=None, current_price=None, previous_close=None, market_cap=None):
        try:
            stock = Stock.objects.get(id=stock_id)
            if symbol is not None:
                stock.symbol = symbol
            if name is not None:
                stock.name = name
            if current_price is not None:
                stock.current_price = current_price
            if previous_close is not None:
                stock.previous_close = previous_close
            if market_cap is not None:
                stock.market_cap = market_cap
            stock.save()
            return stock
        except Stock.DoesNotExist:
            return None

    @staticmethod
    def delete_stock(stock_id):
        try:
            stock = Stock.objects.get(id=stock_id)
            stock.delete()
            return True
        except Stock.DoesNotExist:
            return False

    @staticmethod
    def get_all_stocks():
        return Stock.objects.all()