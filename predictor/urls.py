from django.urls import path
from django.conf.urls import url

from predictor.models import MatchPrediction
from . import views
from .views import (
    predictor_main, 
    matches_page,
    MatchPredictionListView,
    activate,
    logout_view,
    match_prediction,
    MatchPredictionDeleteView,
    MatchPredictionUpdateView,
    )

from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', predictor_main, name='predictor_main'),
    path('matches/', matches_page, name='matches'),
    path('predictions/', MatchPredictionListView.as_view(), name='predictions'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', activate.as_view(), name='activate'), 
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name='logout' ),
    path('<int:pk>/', match_prediction),
    path('predictions/<int:pk>/delete', MatchPredictionDeleteView.as_view(), name='prediction_delete'),
    path('predictions/<int:pk>/edit', MatchPredictionUpdateView.as_view(), name='prediction_update'),
]