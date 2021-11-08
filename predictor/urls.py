from django.urls import path
from .views import predictor_main

urlpatterns = [
    path('', predictor_main, name='predictor_main'),
]