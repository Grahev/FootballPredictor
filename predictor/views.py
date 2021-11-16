from django.contrib.auth.models import User
# from django.core.checks import messages
from django.contrib import messages
from django.shortcuts import render
from .models import League, User, Match, MatchPrediction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView

#pagination import
from django.core.paginator import Paginator

from django.utils import timezone
from django.http import HttpResponseRedirect



#email verification imports
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, MatchPredictionForm
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
            return HttpResponse('Please confirm your email address to complete the registration')  
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

@login_required(login_url='predictor:login')
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
            return redirect("/")


    context = {
        'match':match,
        'form':form,
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