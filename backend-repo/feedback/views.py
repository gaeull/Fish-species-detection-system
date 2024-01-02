from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Feedback
from .serializers import FeedbackSerializer

import boto3
import uuid
from django.conf import settings
from django.core.files.base import ContentFile

class FeedbackView(APIView):
    def post(self, request, Fish_name, format=None):
        description = request.data.get('description')

        try :
            files = request.FILES.getlist('image_url')
            s3_resource = boto3.resource(
                's3', 
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
            )
            key = f"user/{Fish_name}/"

            for file in files :
                file._set_name(str(uuid.uuid4()))
                s3_resource.Bucket('uts-fish-images').put_object( Key=key + '%s'%(file), Body=file, ContentType='image/jpg')
                image_file = ContentFile(file.read())
                Feedback.objects.create(
                    user_fish_name = Fish_name, 
                    user_image_url=f"{settings.AWS_S3_CUSTOM_DOMAIN}{key}{file}",
                    user_description = description
                )
            
            return Response({"MESSGE" : "SUCCESS"}, status=200)
        
        except Exception as e :
            return Response({"ERROR" : str(e)}, status=500)


