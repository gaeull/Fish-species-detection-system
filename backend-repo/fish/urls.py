from django.urls import path
from .views import *

urlpatterns = [
    path('fish/<str:fish_name>', FishDetailView.as_view(), name='fish'),
    path('fish/<str:fish_name>/image', FishImageView.as_view(), name='fish-image'),
]
