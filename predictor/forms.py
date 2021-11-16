from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  
from. models import Player, Team, Match, MatchPrediction
  
class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2')  


class MatchPredictionForm(forms.ModelForm):

    class Meta:
        model = MatchPrediction
        fields = ['homeTeamScore','awayTeamScore','goalScorer']

    def __init__(self, *args, **kwargs):
        ht = kwargs.pop('ht',None)
        at = kwargs.pop('at',None)
        super(MatchPredictionForm,self).__init__(*args, **kwargs)
        self.fields['goalScorer'].queryset= Player.objects.filter(team__in=[ht,at])
        self.fields['homeTeamScore'].label = ht
        self.fields['awayTeamScore'].label = at