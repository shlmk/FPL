import requests
import json

def get_data(fpl_link):
  r = requests.get(fpl_link)

  if r.status_code != 200:
    raise ValueError('Error getting fixtures list')
  else:
    return r.content

if __name__ == "__main__":
  data = get_data('https://fantasy.premierleague.com/drf/fixtures/')

  # https://stackoverflow.com/a/12309296
  with open('fixtures.txt', 'w') as outfile:
    json.dump(data, outfile)
