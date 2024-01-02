from django.urls import path
from .views import Caught_fish_View

urlpatterns = [
    path('caught_fish/', Caught_fish_View.as_view()),
]