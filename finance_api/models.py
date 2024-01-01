from django.db import models
from django.utils import timezone

# Models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Stock(BaseModel):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.TextField(max_length=100)
    stock_price = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.target_date:
            self.target_date = self.start_date + timezone.timedelta(days=30)  # Add one month (approximately 30 days)
        super().save(*args, **kwargs)

class StrategyLeg(models.Model):
    TYPE_CHOICES = [
        ('call', 'Call'),
        ('put', 'Put'),
        ('stock', 'Stock'),
        ('closed', 'Closed'),
    ]
    ACTION_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    strategy = models.ForeignKey('Strategy', related_name='legs', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    strike = models.FloatField(null=True, blank=True)
    premium = models.FloatField(null=True, blank=True)
    n = models.IntegerField()
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    prevpos = models.FloatField()
    expiration = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Strategy(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='strategies')
    strategy_name = models.CharField(default='no-name')
    stockprice = models.FloatField()
    volatility = models.FloatField()
    interestrate = models.FloatField()
    minstock = models.FloatField()
    maxstock = models.FloatField()
    strategy_legs = models.ManyToManyField(StrategyLeg, related_name='strategies')
    dividendyield = models.FloatField(default=0)
    profittarg = models.FloatField(null=True, blank=True)
    losslimit = models.FloatField(null=True, blank=True)
    optcommission = models.FloatField(default=0)
    stockcommission = models.FloatField(default=0)
    compute_the_greeks = models.BooleanField(default=False)
    compute_expectation = models.BooleanField(default=False)
    use_dates = models.BooleanField(default=True)
    discard_nonbusinessdays = models.BooleanField(default=True)
    country = models.CharField(max_length=50, default='US')
    startdate = models.DateField(null=True, blank=True)
    targetdate = models.DateField(null=True, blank=True)
    days2targetdate = models.IntegerField(default=30)
    distribution = models.CharField(max_length=50, default='black-scholes')
    nmcprices = models.IntegerField(default=100000)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class StrategyAnalysisResult(BaseModel):
    strategy = models.ForeignKey('Strategy', related_name='analysis', on_delete=models.CASCADE)
    probability_of_profit = models.FloatField()
    strategy_cost = models.FloatField()
    per_leg_cost = models.TextField()  # JSON representation of list
    profit_ranges = models.TextField()  # JSON representation of list of lists
    minimum_return_in_domain = models.FloatField()
    maximum_return_in_domain = models.FloatField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


"""template[*models.py*]
from django.db import models
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Strategy(models.Model):
    owner = models.ForeignKey('auth.User', related_name='strategies', on_delete=models.CASCADE, default=0)
    pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    action_type = models.CharField(max_length=100, default='call')
    strike = models.FloatField()
    premium = models.FloatField()
    n = models.IntegerField(default=100)
    action = models.CharField(max_length=100, default='sell')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['pinned']"""