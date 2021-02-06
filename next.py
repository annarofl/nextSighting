import requests
import json


location_url = 'http://api.open-notify.org/iss-pass.json'
people_count_url = 'http://api.open-notify.org/astros.json'

parameters = {"lat": 37.78, "lon": -122.41}  # san fran

# Make a get request with the parameters.
response = requests.get(location_url, params=parameters)

json_data = response.json()

pass_overs = json_data['response']  #this is a list of dictionaries on risetime and diration
# times = pass_overs['risetime']
# duration = pass_overs['duration']