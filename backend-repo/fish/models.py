from django.db import models
from caught_fish import *
from datetime import datetime
from django.utils import timezone
class Fish(models.Model):
    fish_name = models.CharField(max_length=50, unique=True)
    E_fish_name = models.CharField(max_length=50, unique=True, default='')
    scientific_name = models.CharField(max_length=50, unique=True)

    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
   
    prohibition_length = models.FloatField(null=True)
    prohibition_region = models.CharField(max_length=225, null=True)
    description = models.CharField(max_length=225)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=True, null=True)

    # foreign키 설정 시, PK의 name으로 보여줌. but db에는 Id로 저장됨.
    # 즉, 객체를 문자열로 표현한걸 반환해줌.
    def __str__(self):
       return self.fish_name
class FishImage(models.Model):
    # N:1 관계인 경우, N모델에서 외래키 정의하면 상대 모델에서의 관계는 자동으로 정의됨.
    fish_id = models.ForeignKey(Fish, on_delete=models.CASCADE, null=True)
    fish_name = models.CharField(max_length=50, unique=True, null=True, default='')
    image_url = models.CharField(max_length=225, null=True, default='')

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

