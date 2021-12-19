import requests
import config
from predictor.models import Player, Team, Match
import json
import time


def get_all_games():
    """get all games"""

    url = 'https://v3.football.api-sports.io/fixtures?league=39&season=2021'
    # url = f'https://v3.football.api-sports.io/players/squads?team={team_id}'
    
    payload={}
    headers = {
      'x-rapidapi-key': config.key,
      'x-rapidapi-host': config.host
    }

    r = requests.request("GET", url, headers=headers, data=payload)
    print(f'request status code:{r.status_code}')
    # file = r'C:\Users\kgrac\Desktop\V2 Football\FootballPredictor\my temp files\all_matches.json'

    data = r.json()

        # Opening JSON file
    # f = open(file)
 
    # returns JSON object as
    # a dictionary
    # data = json.load(data) 
    response = data['response']
    match= response[0]['fixture']
    teams = response[0]['teams']
    
    # print(response)
    for match in response:
        matchday = match['league']['round']
        hTeam = match['teams']['home']['id']
        aTeam = match['teams']['away']['id']
        date = match['fixture']['date']
        status = match['fixture']['status']['short']
        hTeamScore = match['goals']['home']
        aTeamScore = match['goals']['away']
        match_id = match['fixture']['id']

        match = Match.objects.create(
            matchday = matchday,
            hTeam = Team.objects.get(id=hTeam),
            aTeam = Team.objects.get(id=aTeam),
            date = date,
            status = status,
            hTeamScore = hTeamScore,
            aTeamScore = aTeamScore,
            match_id = match_id
        )
        match.save()
        print(f'{hTeam} : {aTeam} status: {status} added to db')

def run():
    get_all_games()