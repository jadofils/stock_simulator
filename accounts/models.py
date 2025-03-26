# accounts/models.py
from django.db import models

# USER model
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    #table name

    class Meta:
        db_table = 'users'
        unique_together = ('username', 'email')



# USER_PROFILE model
class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    total_investment = models.DecimalField(max_digits=10, decimal_places=2)
    total_profit_loss = models.DecimalField(max_digits=10, decimal_places=2)

    #table name
    class Meta:
        db_table = 'user_profiles'
        unique_together = ('user',)


# STOCK model
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    previous_close = models.DecimalField(max_digits=10, decimal_places=2)
    market_cap = models.DecimalField(max_digits=15, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    #table name
    class Meta:
        db_table = 'stocks'
        unique_together = ('symbol',)
       

# PORTFOLIO model
class Portfolio(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    #table name
    class Meta:
        db_table = 'portfolios'
        unique_together = ('user', 'stock')
        ordering = ['-purchase_date']



# WATCHLIST model


# TRANSACTION model
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)  # Buy/Sell
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    total_value = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    #table name
    class Meta:
        db_table = 'transactions'
        ordering = ['-timestamp']
        unique_together = ('user', 'stock', 'transaction_type', 'timestamp')
        indexes = [
            models.Index(fields=['user', 'transaction_type', 'timestamp']),
            models.Index(fields=['user', 'stock', 'transaction_type']),
        ]


# STOCK_PRICE_HISTORY model
class StockPriceHistory(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    class Meta:
        db_table = 'stock_price_histories'
        unique_together = ('stock', 'date')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['stock', 'date']),
        ]
