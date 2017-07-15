import requests
import json
import os.path

def get_data(fpl_link):
  r = requests.get(fpl_link)

  if r.status_code != 200:
    raise ValueError('Error getting fixtures list')
  else:
    return r.content

if __name__ == "__main__":
  # https://stackoverflow.com/a/82852
  if not os.path.isfile('raw-data/fixtures.txt'):
    data = json.loads(get_data('https://fantasy.premierleague.com/drf/fixtures/'))
    # https://stackoverflow.com/a/12309296
    with open('raw-data/fixtures.txt', 'w') as outfile:
      json.dump(data, outfile)

  if not os.path.isfile('raw-data/teams.txt'):
    data = json.loads(get_data('https://fantasy.premierleague.com/drf/bootstrap-static'))

    with open('raw-data/teams.txt', 'w') as outfile:
      json.dump(data['teams'], outfile)

  #https://stackoverflow.com/a/2835672
  with open('raw-data/fixtures.txt') as fixtures:
    fixture_data = json.load(fixtures)

  with open('raw-data/teams.txt') as teams:
    team_data = json.load(teams)

  teams = [team['name'] for team in team_data]
  fixture_dict = {team: {'opponent':[], 'difficulty':[]} for team in teams}
