from django.db import models
from django.utils import timezone
from fish.models import Fish

# Create your models here.
class Caught_fish(models.Model):
    fish_name = models.CharField(max_length=50, unique=True)
    fish_length = models.FloatField(null=True)
    user_region = models.CharField(max_length=225, null=True)
    image_url = models.CharField(max_length=225, null=True)
    description = models.CharField(max_length=400, null=True)
    
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)


    