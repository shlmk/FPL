import requests

def get_data(fpl_link):
  r = requests.get(fpl_link)

  if r.status_code != 200:
    raise ValueError('Error getting fixtures list')
  else:
    print(r.content)

get_data('https://fantasy.premierleague.com/drf/fixtures/')
