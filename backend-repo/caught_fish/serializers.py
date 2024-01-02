from rest_framework import serializers

from .models import Caught_fish


class CaughtFishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caught_fish
        fields = ('fish_length', 'user_region', 'image_url', 'main_fish_id','main_fish_id', 'main_fish_accuracy', 'sub1_fish_id', 'sub1_fish_accuracy', 'sub2_fish_id', 'sub2_fish_accuracy')    
         
        
