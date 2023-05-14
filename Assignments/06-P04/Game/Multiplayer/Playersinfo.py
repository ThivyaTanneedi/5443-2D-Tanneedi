import requests

#------------------------------------------------------------------------
# Description
#       Returns a list of the players being used on the server
#
def get_used_players():
    res = requests.get('https://terrywgriffin.com/current_usage.json')
    used_players = res.json()
    return used_players['players']