import config
import requests
from predictor.models import Team
import json



def get_teams():
    """get all teams and add them to Team model in database"""

    url = 'https://v3.football.api-sports.io/teams?league=2&season=2021'
    
    payload={}
    headers = {
      'x-rapidapi-key': config.key,
      'x-rapidapi-host': config.host
    }

    r = requests.request("GET", url, headers=headers, data=payload)

    data = r.json()
  
    response = data['response']

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