from django.db import models
from django.utils import timezone

class BaseModel(models.Model): # Not in use!
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
        ordering = ['pinned']