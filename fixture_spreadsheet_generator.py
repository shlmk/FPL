import argparse
import requests
import json
import os.path
from copy import deepcopy
from create_spreadsheet import create_spreadsheet

'''
  Parsers commandline arguments to generate spreadsheet. Options user can
  select are: the filename of the spreadsheet, what sheets to include,
  and whether to override raw and processed data folders
'''
def parse_arguments():
  parser = argparse.ArgumentParser(description='Generate FPL Fixture Spreadsheet')
  parser.add_argument('spreadsheet_filename', type=str, nargs='?', default='fixtures',
                      help='the spreadsheet filename (e.g. fixtures); .xlsx will be appended for you')
  parser.add_argument('sheets', choices=['all', 'opponents', 'difficulty'],
                    help='type of sheet you want included. Options are all,' +
                    ' opponents, or difficulty')
  parser.add_argument('--override', dest='override', action='store_true',
                      help='whether to override the raw and processed data (if it exists)')
  return parser

'''
  Gets data at a specific url from fpl website.
  @param   fpl_link   URL to get data from
  @return             json representation of premier league fixtures otherwise
                      an error
'''
def get_data_from_fpl(fpl_link):
  r = requests.get(fpl_link)

  if r.status_code != 200:
    raise ValueError('Error getting fixtures list')
  else:
    return json.loads(r.content)

'''
  Writes the list of teams to a text file in the raw_data directory
'''
def write_teams_txt():
  data = get_data_from_fpl('https://fantasy.premierleague.com/drf/bootstrap-static')
  # https://stackoverflow.com/a/12309296
  with open('raw_data/teams.txt', 'w') as outfile:
    json.dump(data['teams'], outfile)

'''
  Writes all of the fixtures (with all FPL info) to a text file under the
  raw_data directory
'''
def write_fixtures_txt():
  data = get_data_from_fpl('https://fantasy.premierleague.com/drf/fixtures/')
  with open('raw_data/fixtures.txt', 'w') as outfile:
    json.dump(data, outfile)

'''
  Gets the data from a particular text file
  @param    filename    the file you wish to you open
  @return               json representation of the data in the file
'''
def get_data_from_txt(filename):
  with open(filename) as data:
    return(json.load(data))

'''
  Creates a new (deep copy) list of fixtures with team ids replaced by the
  actual team names
  @param  teams     An alphabetically sorted list of all 20 Premier League teams
  @param  fixtures  A list of all fixtures
  @return           Deep copy of fixture list with team names rather than team ids
'''
def convert_fixture_ids_to_teams(teams, fixtures):
  new_fixtures = deepcopy(fixtures)

  for fixture in new_fixtures:
     home_id = fixture['team_h']
     away_id = fixture['team_a']
     fixture['team_h'] = teams[home_id - 1]
     fixture['team_a'] = teams[away_id - 1]

  return new_fixtures

'''
  Processes the list of fixtures and returns a processed dictionary of opponents
  and difficulty level for each team
  @param    teams     An alphabetically sorted list of all 20 Premier League teams
  @param    fixtures  A list of all 380 fixtures in JSON format
  @return             A dictionary with list of opponents and corresponding
                      difficulty in chronological order
'''
def process_fixtures(teams, fixtures):
  processed_dict = {team: {'opponents':[], 'difficulty':[]} for team in teams}

  for fixture in fixtures:
    home_team = fixture['team_h']
    away_team = fixture['team_a']
    home_diff = fixture['team_h_difficulty']
    away_diff = fixture['team_a_difficulty']

    processed_dict[home_team]['opponents'].append(away_team + ' (H)')
    processed_dict[home_team]['difficulty'].append(str(home_diff) + ' (H)')
    processed_dict[away_team]['opponents'].append(home_team + ' (A)')
    processed_dict[away_team]['difficulty'].append(str(away_diff) + ' (A)')

  return processed_dict

if __name__ == "__main__":
  parser = parse_arguments()
  args = parser.parse_args()

  spreadsheet_filename = args.spreadsheet_filename
  sheets = args.sheets
  override = args.override

  '''
    Raw data section
  '''
  # https://stackoverflow.com/a/273227
  # see discussion (I can get away because no race condition)
  if not os.path.exists('raw_data'):
    os.makedirs('raw_data')

  if not os.path.isfile('raw_data/teams.txt') or override:
    write_teams_txt()

  if not os.path.isfile('raw_data/fixtures.txt') or override:
    write_fixtures_txt()

  '''
    Processed data section
  '''
  if not os.path.exists('processed_data'):
    os.makedirs('processed_data')

  if not os.path.exists('processed_data/team_schedules.txt') or override:
    team_data = get_data_from_txt('raw_data/teams.txt')
    fixture_data = get_data_from_txt('raw_data/fixtures.txt')

    # Included to deal with bad data of fixture ids in the wrong order
    fixture_data = sorted(fixture_data, key=lambda k: k['id'])

    teams = [team['name'] for team in team_data]
    fixture_with_teams = convert_fixture_ids_to_teams(teams, fixture_data)
    complete_fixtures = process_fixtures(teams, fixture_with_teams)

    with open('processed_data/team_schedules.txt', 'w') as outfile:
      json.dump(complete_fixtures, outfile)

    create_spreadsheet('fixtures.xls', complete_fixtures)

  else:
    with open('processed_data/team_schedules.txt') as team_fixtures:
      create_spreadsheet(spreadsheet_filename + '.xlsx',  json.load(team_fixtures), sheets)
