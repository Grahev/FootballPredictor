from django.urls import path
from django.conf.urls import url
from . import views
from .views import (
    predictor_main, 
    matches_page,
    MatchPredictionListView,
    activate,
    logout_view
    )

from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', predictor_main, name='predictor_main'),
    path('matches/', matches_page, name='matches'),
    path('predictions/', MatchPredictionListView.as_view(), name='predictions'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', activate.as_view(), name='activate'), 
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name='logout' )
]