import requests
import config
from predictor.models import Match, MatchEvents, Team, Player





def match_update(event_id):
    #event_id = '710676'
    url = f'https://v3.football.api-sports.io/fixtures?id={event_id}'

    payload={}
    headers = {
      'x-rapidapi-key': config.key,
      'x-rapidapi-host': config.host
    }
    r = requests.request("GET", url, headers=headers, data=payload)
    print(f'request status code:{r.status_code}')

    data = r.json()

    response = data['response']

    
    hTeamScore = response[0]['goals']['home']
    if hTeamScore:
        print('score not null')
    else:
        hTeamScore = 0
    aTeamScore = response[0]['goals']['away']
    if aTeamScore:
        print('score not null')
    else:
        aTeamScore = 0
    status = response[0]['fixture']['status']['short']
    events = response[0]['events']
    
    #update match score and status
    if status == 'FT':
        m = Match.objects.get(match_id=event_id)
        m.hTeamScore = int(hTeamScore)
        m.aTeamScore = int(aTeamScore)
        m.status = status
        m.save()
        print(f'match scores updated {m}')
    else:
        print('match not finished')
        m = Match.objects.get(match_id=event_id)
        m.status = status
        m.save()
        print(f'match status updated {m}')
    
    #create goal events for match
    for event in events:
        match_id = event_id
        team_id = event['team']['id']
        time = event['time']['elapsed']
        player_id = event['player']['id']
        e_type = event['type']

        #print(f'match id:{match_id}, team id: {team_id}, time:{time}, player id:{player_id}, type:{e_type}')

        if player_id:
            if e_type == 'Goal':
                #print(m)
                m.goalScorers.add(Player.objects.get(player_id=player_id)) #add goalscorers to match goalscorers (many to many field)
                #create event object with all goals 
                match_event = MatchEvents.objects.create(
                    match = Match.objects.get(match_id=match_id),
                    team = Team.objects.get(id=team_id),
                    time = time,
                    player = Player.objects.get(player_id=player_id),
                    type = e_type,
                )
                match_event.save()
                print('Match event created')
                print('goal scorer added')
            else:
                print('no goal event')
        else:
            continue
        


def run():
    all_matches = Match.objects.filter(status='NS').order_by('matchday')
    matchday = all_matches.first().matchday

    current_matchday = all_matches.filter(matchday=matchday) #get queryset only for last not finished matchday

    for match in current_matchday:
        if match.status == 'NS':
            match_update(match.match_id)
            print('match updated')
        else:
            continue