from django.conf import settings
from rest_framework import serializers
from .models import *

class FishImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishImage
        fields = ('fish_id', 'image_url')
        
class FishSerializer(serializers.ModelSerializer):
    fish_images = FishImageSerializer(many=True, source='fishimage_set')
    class Meta:
        model = Fish
        fields = (
            'fish_name', 
            'scientific_name', 
            'start_date', 
            'end_date', 
            'prohibition_length', 
            'prohibition_region', 
            'description',
            'fish_images',
            'E_fish_name'
        )

    def create(self, validated_data):
        fish = Fish.objects.create(**validated_data)
        return fish

    def update(self, instance, validated_data):
        instance.fish_name = validated_data.get('fish_name', instance.fish_name)
        instance.scientific_name = validated_data.get('scientific_name', instance.scientific_name)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.prohibition_length = validated_data.get('prohibition_length', instance.prohibition_length)
        instance.prohibition_region = validated_data.get('prohibition_region', instance.prohibition_region)
        instance.description = validated_data.get('description', instance.description)
        instance.fish_images = validated_data.get('fish_images', instance.fish_images)
        instance.save()
        return instance

    def delete(self, instance):
        instance.is_deleted = True
        instance.save()


