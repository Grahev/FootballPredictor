import requests
from predictor.models import MatchEvents, MatchPrediction
import config
from predictor.models import Match


def goalscorers():
    goals = MatchEvents.objects.filter(match=Match.objects.get(match_id=710740)).order_by('time')

    print(len(goals))
    for g in goals:
        print(g.player)


goalscorers()