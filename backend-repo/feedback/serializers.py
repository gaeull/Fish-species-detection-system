from django.conf import settings
from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('user_fish_name', 'user_image_url', 'user_description')