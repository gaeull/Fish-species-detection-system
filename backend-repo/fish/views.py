from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from rest_framework import status

from .models import Fish, FishImage
from .serializers import *

import boto3
import uuid
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist

class FishDetailView(APIView):
    def get(self, request, fish_id, format=None):
        # print(request)
        try:
            fish = Fish.objects.get(id=fish_id)
        except Fish.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        fish_serializer = FishSerializer(fish)

        return Response({"fish": fish_serializer.data})

class FishImageView(APIView): 
    def post(self, request, fish_name, format=None):
        try:
            fish = Fish.objects.get(fish_name=fish_name)
        except ObjectDoesNotExist:
            return Response({"ERROR": "Fish not found"}, status=404)
        
        try :
            files = request.FILES.getlist('files')
            s3_resource = boto3.resource(
                's3', 
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
            )
            key = f"fish/{fish_name}/"

            for file in files :
                file._set_name(str(uuid.uuid4()))
                s3_resource.Bucket('uts-fish-images').put_object( Key=key + '%s'%(file), Body=file, ContentType='image/jpg')
                image_file = ContentFile(file.read())
                FishImage.objects.create(
                    fish_name=fish_name, 
                    image_url=f"{settings.AWS_S3_CUSTOM_DOMAIN}{key}{file}"
                )
            
            return Response({"MESSGE" : "SUCCESS"}, status=200)
        
        except Exception as e :
            return Response({"ERROR" : str(e)}, status=500)


