import requests
import json
from datetime import datetime
import location
import secrets


def get_ISS_times(latitude, longitude, url):

    parameters = {"lat": latitude, "lon": longitude}

    response = requests.get(url, params=parameters)

    json_data = response.json()

    pass_overs = json_data['response']

    return pass_overs


def compose_msg(lst, address):
    msg = "The next {0} sightings of the International Space Station at {1} will be on: \n".format(len(lst), address)
    for r in lst:
        date = datetime.utcfromtimestamp(r['risetime']).strftime('%m-%d-%Y')
        time = datetime.utcfromtimestamp(r['risetime']).strftime("%I:%M %p")
        m = str(r['duration'] // 60)
        s = str(r['duration'] % 60)
        m = "{0} at {1} for {2} minutes {3} seconds. \n".format(date, time, m, s)
        msg += m

    slack_data = {
        "text": msg
        }

    response = requests.post(
        secrets.SLACK_URL, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )


if __name__ == "__main__":
    df = location.pull_address_list()

    df = location.convert_lon_lat(df)

    location_url = 'http://api.open-notify.org/iss-pass.json'

    #todo: another call to get number of people on ISS
    people_count_url = 'http://api.open-notify.org/astros.json'

    # df['passovers'] is a list of dictionaries on risetime and duration
    df['passovers'] = df.apply(lambda x: get_ISS_times(x['latitude'], x['longitude'], location_url), axis=1)

    df['msg'] = df.apply(lambda x: compose_msg(x['passovers'], x['ADDRESS']), axis=1)