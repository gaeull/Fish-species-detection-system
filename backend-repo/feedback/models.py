from django.db import models

class Feedback(models.Model):
    user_fish_name = models.CharField(max_length=50, null=True)
    user_image_url = models.CharField(max_length=225, null=True)
    user_description = models.CharField(max_length=225, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=True, null=True)
