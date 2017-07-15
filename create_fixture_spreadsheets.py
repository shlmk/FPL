import requests
import json
import os.path
from copy import deepcopy

def get_data(fpl_link):
  r = requests.get(fpl_link)

  if r.status_code != 200:
    raise ValueError('Error getting fixtures list')
  else:
    return r.content

def convert_fixture_ids_to_teams(fixtures, teams):
  new_fixtures = deepcopy(fixtures)

  for fixture in new_fixtures:
     home_id = fixture['team_h']
     away_id = fixture['team_a']
     fixture['team_h'] = teams[home_id - 1]
     fixture['team_a'] = teams[away_id - 1]

  return new_fixtures

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

  fixture_with_teams = convert_fixture_ids_to_teams(fixture_data, teams)

  for fixture in fixture_with_teams:
    home_team = fixture['team_h']
    away_team = fixture['team_a']
    home_diff = fixture['team_h_difficulty']
    away_diff = fixture['team_a_difficulty']

    fixture_dict[home_team]['opponent'].append(away_team + ' (H)')
    fixture_dict[home_team]['difficulty'].append(home_diff)
    fixture_dict[away_team]['opponent'].append(home_team + ' (A)')
    fixture_dict[away_team]['difficulty'].append(away_diff)

  #https://stackoverflow.com/a/273227 -- see discussion (I can get away because no race condition)
  if not os.path.exists('processed-data'):
    os.makedirs('processed-data')

  with open('processed-data/team_schedules.txt', 'w') as outfile:
    json.dump(fixture_dict, outfile)
