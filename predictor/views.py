from django.contrib.auth.models import User
from django.shortcuts import render
from .models import League, User, Match, MatchPrediction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView

#pagination import
from django.core.paginator import Paginator

# Create your views here.

def predictor_main(request):
    leagues = League.objects.all().filter(admin= User.objects.get(username="admin") )
    context = {
        'leagues': leagues
    }
    return render(request,'predictor/predictor_main.html', context)



def matches_page(request):
    matches = Match.objects.all().order_by('id')
    p = Paginator(matches,10)
    page = request.GET.get('page')
    games = p.get_page(page)
    context = {
        'games' : games,
    }

    return render(request, 'predictor/matches.html', context)


class MatchPredictionListView(LoginRequiredMixin,ListView):
    model = MatchPrediction
    template_name = "predictor/predictions_list.html"
    context_object_name = 'predictions'
    # ordering = ['-date_created']
    
    def get_queryset(self):
        return MatchPrediction.objects.filter(user = self.request.user)