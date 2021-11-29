import requests
from predictor.models import MatchEvents, MatchPrediction
import config
from predictor.models import Match



def match_one_x_two(prediction):
    """return 1 X 2 for match"""
    if prediction.match.hTeamScore > prediction.match.aTeamScore:
        match_winner = '1'
    elif prediction.match.hTeamScore == prediction.match.aTeamScore:
        match_winner = 'X'
    elif prediction.match.hTeamScore < prediction.match.aTeamScore:
        match_winner = '2'
    return match_winner

def prediction_one_x_two(prediction):
    """return 1 X 2 for match prediction"""
    if prediction.homeTeamScore > prediction.awayTeamScore:
        prediction_winner = '1'
    elif prediction.homeTeamScore == prediction.awayTeamScore:
        prediction_winner = 'X'
    elif prediction.homeTeamScore < prediction.awayTeamScore:
        prediction_winner = '2'
    return prediction_winner

def run():
  unchacked_predictions = MatchPrediction.objects.filter(checked=False)

  for prediction in unchacked_predictions:
    points = 0
    goal_scorers = MatchEvents.objects.filter(match=prediction.match).order_by('time')
   
    
    if goal_scorers[0].player.name == prediction.goalScorer.name:
      points+=3
      print('3 points for correct first goalscorer')
    else:
      for goal in goal_scorers:
        if goal.player.name == prediction.goalScorer.name:
          print('1 point for anytime goalscorer')
          points +=1
          break
        else:
          continue

    if prediction.homeTeamScore == prediction.match.hTeamScore and prediction.awayTeamScore == prediction.match.aTeamScore:
      points +=3
      print('3 points for correct score')
    else: 
      match_winner = match_one_x_two(prediction)
      prediction_winner = prediction_one_x_two(prediction)
      if match_winner == prediction_winner:
        points +=1
        print('1 point for winner')
      else:
        points +=0

    p = MatchPrediction.objects.filter(pk=prediction.pk)
    p.update(points=points, checked=True)
    print(f'points: {points} - {p} updated')

    
    
    
    
    
    
    
    
    
    # print(prediction.match)
    # for goal in goal_scorers:
    #   print(f'{goal.player.name} minute: {goal.time}')

  print(unchacked_predictions)

    
