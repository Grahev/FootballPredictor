import config
import requests
from predictor.models import Team
import json
import os



def get_teams():
    """get all teams and add them to Team model in database"""

    url = 'https://v3.football.api-sports.io/teams?league=39&season=2021'
    
    payload={}
    headers = {
      'x-rapidapi-key': os.environ.get('API_KEY','dev default value'),
      'x-rapidapi-host': os.environ.get('API_HOST','dev default value')
    }

    r = requests.request("GET", url, headers=headers, data=payload)
    # file = r'C:\Users\kgrac\Desktop\V2 Football\FootballPredictor\my temp files\epl teams.json'

    data = r.json()
    # json_obj = file.json()
    # teams = json_obj['teams']
    # for team in teams:
    #     name = team['name']
    #     team_id = team['id']
    #     shortName = team['shortName']
    #     tla = team['tla']
    #     website = team['website']
    #     crestUrl = team['crestUrl']
    #     #team = Team.objects.create(name=name,team_id=team_id,shortName=shortName,tla=tla,website=website,crestUrl=crestUrl)
    #     team.save()
    #     print(f'{name} added to DB')


    # Opening JSON file
    # f = open(file)
 
    # returns JSON object as
    # a dictionary
    # data = json.load(f) 
    response = data['response']
    print(response)

    for i in response:
        id = i['team']['id']
        name = i['team']['name']
        country = i['team']['country']
        founded = i['team']['founded']
        logo = i['team']['logo']
        team = Team.objects.create(id=id,name=name,country=country,founded=founded,logo=logo)
        team.save()
        print(f'{name} created and saved in database')


get_teams()