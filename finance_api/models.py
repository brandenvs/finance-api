from django.db import models
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
        # Check if target_date is not explicitly set, and set it one month ahead of start_date
        if not self.target_date:
            self.target_date = self.start_date + timezone.timedelta(days=30)  # Add one month (approximately 30 days)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.symbol


class Strategy(BaseModel):
    created_by = models.ForeignKey('auth.User', related_name='strategies', on_delete=models.CASCADE, default=0)
    name = models.CharField(blank=False, max_length=100)
    description = models.TextField(blank=True, null=True)

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)


    
    premium = models.FloatField(blank=True, default=0.0)
    options = models.ManyToManyField(Option)
    
    def __str__(self):
        return self.name

class ProbabilityOfProfit(BaseModel):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    calculation = models.ForeignKey(FinancialCalculator, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=4)
    calculation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.strategy} - {self.calculation_date}"

# from django.db import models
# from django.db import models
# from django.utils import timezone


# class BaseModel(models.Model):
#     created_at = models.DateTimeField(db_index=True, default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True

# class Strategy(models.Model):
#     owner = models.ForeignKey('auth.User', related_name='strategies', on_delete=models.CASCADE, default=0)
#     pinned = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     title = models.CharField(max_length=100)
#     action_type = models.CharField(max_length=100, default='call')
#     strike = models.FloatField()
#     premium = models.FloatField()
#     n = models.IntegerField(default=100)
#     action = models.CharField(max_length=100, default='sell')

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#     class Meta:
#         ordering = ['pinned']