from django.urls import path
from .views import *

urlpatterns = [
    path('fish/user/<str:Fish_name>', FeedbackView.as_view(), name='Feedback')
]
