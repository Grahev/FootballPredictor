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
    LeagueCreateView,
    league_view,
    league_details,
    join_league,
    join_league_pin,
    leave_league,
    leave_league_confirm,
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
    path('leagues/create', LeagueCreateView.as_view(), name='create_league'),
    path('leagues/', league_view, name='leagues'),
    path('leagues/<int:pk>/', league_details, name='league_details'),
    path('leagues/join', join_league, name='join_league'),
    path('leagues/join/<int:pk>', join_league_pin, name='join_league'),
    path('leagues/leave/<int:pk>', leave_league, name='leave_league'),
    path('leagues/leave/confirm/<int:pk>', leave_league_confirm, name='leave_league_confirm'),
]