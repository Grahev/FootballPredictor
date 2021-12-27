from django.db import models
from django.db.models.deletion import CASCADE, SET, SET_NULL
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    founded = models.IntegerField()
    logo = models.CharField(max_length=250)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Player(models.Model):
    player_id = models.IntegerField()
    name = models.CharField(max_length=50)
    age = models.IntegerField(null=True)
    number = models.IntegerField(null=True)
    position = models.CharField(max_length=50)
    photo = models.CharField(max_length=250)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        ordering = ('team__name', 'position','name')

    def __str__(self):
        return f'{self.team} - {self.name}'



class Match(models.Model):

    matchday = models.CharField(max_length=50)
    hTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    aTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    date = models.DateTimeField()
    status = models.CharField(max_length=20)
    hTeamScore = models.IntegerField(blank=True, null=True)
    aTeamScore = models.IntegerField(blank=True, null=True)
    goalScorers = models.ManyToManyField(Player, related_name='goal_scorers',blank=True,null=True)
    match_id = models.IntegerField()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'MD{self.matchday} - {self.hTeam} : {self.aTeam} - {self.status}'

    @property
    def is_past_due(self):
        return timezone.now() > self.date

    @property
    def md(self):
        day = self.matchday.split('-')[-1]
        return day

    @property
    def first_goal(self):
        first = MatchEvents.objects.filter(match=self).first()
        f = first.player.name
        return f

class MatchEvents(models.Model):
    match = models.ForeignKey(Match, on_delete=CASCADE)
    team = models.ForeignKey(Team, on_delete=CASCADE)
    time = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=CASCADE)
    type = models.CharField(max_length=50)



class MatchPrediction(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    homeTeamScore = models.PositiveIntegerField()
    awayTeamScore = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goalScorer = models.ForeignKey(Player, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
    points = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return f'MD:{self.pk}-{self.match.matchday}-{self.user}-{self.match.hTeam} {self.homeTeamScore} : {self.awayTeamScore} {self.match.aTeam}'

    @property
    def is_past_due(self):
        return timezone.now() > self.match.date


class League(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    pin = models.IntegerField(max_length=6)
    admin = models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name='league_admin')
    users = models.ManyToManyField(User, related_name='league_users')
    create_date = models.DateTimeField(auto_now_add=True)
    rules = models.TextField(max_length=500, blank=True)
    

    def __str__(self):
        return self.name