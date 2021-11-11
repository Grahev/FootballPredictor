from django.urls import path
from .views import (
    predictor_main, 
    matches_page,
    MatchPredictionListView,
    )

urlpatterns = [
    path('', predictor_main, name='predictor_main'),
    path('matches/', matches_page, name='matches'),
    path('predictions/', MatchPredictionListView.as_view(), name='predictions'),
]