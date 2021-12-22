from django.contrib.auth.models import User
# from django.core.checks import messages
from django.contrib import messages
from django.forms import fields
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import League, User, Match, MatchPrediction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView, DetailView

#pagination import
from django.core.paginator import Paginator

from django.utils import timezone
import datetime
from django.http import HttpResponseRedirect

#api import
# import config
import os


#email verification imports
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, MatchPredictionForm, LeagueJoinPinForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import generate_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required





# Create your views here.

def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            # message = render_to_string('acc_active_email.html', {  
            message = render_to_string('activate.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':generate_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please go to your email and confirm your email address by click activation link from email to complete the registration')  
    else:  
        form = SignupForm()  
    return render(request, 'signup.html', {'form': form})  


class activate(View):
    def get(self, request,uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
           # messages.add_message(request, messages.INFO,'account activated sucesfully')
            return redirect ('predictor:login') #change to login 
        return render(request,'activate_failed.html', status=401) 

def logout_view(request):
    logout(request)
    return redirect('/')

# @login_required(login_url='predictor:login')
def predictor_main(request):
    leagues = League.objects.all().filter(admin= User.objects.get(username="admin") )
    context = {
        'leagues': leagues
    }
    return render(request,'predictor/predictor_main.html', context)


@login_required(login_url='predictor:login')
def matches_page(request):
    matches = Match.objects.all().order_by('id')
    ns_matches = Match.objects.filter(status='NS')
    md = ns_matches.first()
    upcoming_matches = ns_matches.filter(matchday=md.matchday)
    print(upcoming_matches)
    p = Paginator(ns_matches,10)
    page = request.GET.get('page')
    games = p.get_page(page)
    context = {
        # 'games' : games,
        'games' : upcoming_matches,
    }

    return render(request, 'predictor/matches.html', context)




class MatchPredictionListView(LoginRequiredMixin,ListView):
    model = MatchPrediction
    template_name = "predictor/predictions_list.html"
    context_object_name = 'predictions'
    
    
    def get_queryset(self):
        return MatchPrediction.objects.filter(user = self.request.user).order_by('-match__date')



def match_prediction(request,pk):
    match = Match.objects.get(id=pk)
    form = MatchPredictionForm()
    md = match.matchday
    hteam = match.hTeam
    ateam = match.aTeam
    form = MatchPredictionForm(ht=hteam,at=ateam)
    m_id = match.match_id
    # key = config.key
    key = os.environ.get('key')
    print(m_id)


    print(match.date)
    print(timezone.now())
    if match.date < timezone.now():
        print('matchday is smaller')
    else:
        print('time now is bigger')


    if request.method == 'POST':
        pred = MatchPrediction.objects.filter(user=request.user).filter(match__in=Match.objects.filter(id=pk)).exists()
        print(pred)
        print('post request')
        form = MatchPredictionForm(request.POST,ht=hteam,at=ateam)
        if form.is_valid():
            if pred == True:
                messages.error(request,'Prediction for this match alerady exists, please make prediction for other match.')
                return HttpResponseRedirect(request.path_info)
            if MatchPrediction.objects.filter(user = request.user).filter(match__in=Match.objects.filter(matchday=md)).count() >= 3:
                print('if statment')
                # print(MatchPrediction.objects.filter(user = request.user).filter(match__in=Match.objects.filter(matchday=md)).count())
                messages.error(request,'You predict 3 games already, delete your prediction to make new for this matchday.')
                return HttpResponseRedirect(request.path_info)
            if match.date < timezone.now():
                messages.error(request,'Prediction match alredy started and can NOT be added on or edited. Please do prediction for other match.')
                return HttpResponseRedirect(request.path_info)

            print(form.cleaned_data)
            homeTeamScore = form.cleaned_data['homeTeamScore']
            awayTeamScore = form.cleaned_data['awayTeamScore']
            goal = form.cleaned_data['goalScorer']
            user = request.user.username
            print(goal)
            u = User.objects.get(username=user)
            MatchPrediction.objects.create(
                match = match,
                homeTeamScore=homeTeamScore,
                awayTeamScore=awayTeamScore,
                user = u,
                goalScorer = goal,
            )
            print('new prediction created')
            return redirect("/matches")


    context = {
        'match':match,
        'form':form,
        'key':key,
    }
    return render(request, 'predictor/match_prediction.html', context)


class MatchPredictionDeleteView(DeleteView):
    model = MatchPrediction
    template_name = "predictor/prediction_delete.html"
    success_url = "/predictions/"

class MatchPredictionUpdateView(UpdateView):

    model = MatchPrediction
    template_name = 'predictor/prediction_edit.html'
    context_object_name = 'prediction'
    form = MatchPredictionForm()
    model = MatchPrediction
    fields = ['homeTeamScore','awayTeamScore','goalScorer']
    success_url = '/predictions/'

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['key'] =  config.key
        context['key'] = os.environ.get('key')
        print(context)
        return context


class LeagueCreateView(CreateView):
    model = League
    template_name = 'predictor/league_create.html'
    fields = ['name','pin','rules']
    success_url = '/leagues/'


def league_view(request):
    """view for list of users leagues"""
    user = request.user.username
    leagues = League.objects.filter(users=User.objects.get(username=user))
    context = {
        'leagues':leagues,
    }
    return render(request, 'predictor/league.html', context)

def league_details(request,pk):
    league = League.objects.get(id=pk)
    table = []
    create_date = league.create_date

    #create dict with user points
    for user in league.users.iterator():  
        points_dict = {}
        user_points = 0
        #print(user)
        predictions = MatchPrediction.objects.filter(user=user).filter(match__date__gte = create_date)
        print(predictions)
        for match in predictions.iterator():
            if match.points:
                print(match.points)
                user_points += match.points
        print(f'{user} points:{user_points}')
        points_dict = {
            'name': user.username,
            'points' : user_points
            }

        table.append(points_dict)
    
    #sort table by points
    points_table= sorted(table, key=lambda d: d['points'], reverse=True)
    
    context = {
        'league': league,
        'table' : points_table,
    }

    return render(request,'predictor/league_details.html', context)


def join_league(request):
    print(request.POST)
    leagues = League.objects.all()
    

    if request.method == 'POST':
        form = request.POST
        try:
            league = League.objects.get(name=form['name'])
            print(league.admin)
        except:
            league = ''
        
   


    context = {
        'leagues':leagues
    }
    return render(request,'predictor/join_league.html', context)

def join_league_pin(request, pk):
    league = League.objects.get(id=pk)
    form = LeagueJoinPinForm()
    user = request.user
    print(league)

    if request.method == 'POST':
        form = LeagueJoinPinForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data['pin']
            print(f'pin: {type(pin)}')
            print(f'league pin:{league.pin}')
            if pin == league.pin:
                print('match')
                league.users.add(user)
                messages.info(request,f'You join {league.name}.')
                return redirect('/leagues')
            else:
                print('pin not match')

    context = {
        'league':league,
        'form': form
    }
    return render(request,'predictor/join_league_confirm.html',context)




def leave_league(request,pk):
    league = League.objects.get(id=pk)
    user = request.user

    print(league)

    context = {
        'league': league
    }

    return render(request,'predictor/leave_league.html', context)

def leave_league_confirm(request,pk):
    league = League.objects.get(id=pk)
    user = request.user

    if league.name == 'MASTER LEAGUE':
        messages.error(request, 'You cant leave MASTER LEAGUE')
        return redirect('/leagues')
    else:
        league.users.remove(user)
        messages.info(request,f'You leave {league.name}.')
        return redirect('/leagues')

def user_predictions_list(request, user):
    predictions = MatchPrediction.objects.filter(user__username = user).order_by('-match__status','-match__matchday')
    context = {
        'predictions': predictions
    }
    return render(request, 'predictor/user_predictions_list.html', context)