from .get_teams import get_teams
from .get_players import get_players_run
from .get_all_games import get_all_games


def run():
    get_teams()
    print('teams added')
    get_players_run()
    print("players added")
    get_all_games()
    print("all matches added")
    print("FINISH")


run()