import requests
import json
import datetime
import logging
from api.firebase import Firebase
import os
import sec

# todo add docker secrets
logger = logging.getLogger('gdelt_retrieval_service')


class GoogleBigQuery:
    def __init__(self):
        self.base_google_url = os.getenv('base_google_url')
        self.google_auth_url = os.getenv('google_auth_url', 'http://google.com')
        self.google_client_id = os.getenv('google_client_id')
        # sec.load leverages docker vault for secret managerment rather than having secrets in os variables.
        self.google_client_secret = sec.load('google_client_secret')
        self.refresh_token = sec.load('refresh_token')

        self.endpoint = os.getenv('google_endpoint', '')

    def get_gdelt_data(self, index):

        auth_token = self.get_access_token()
        header = {'Authorization': 'Bearer ' + auth_token}

        params = {
            'selectedFields': 'GoldsteinScale, AvgTone, Actor1Code, Actor1Geo_Lat, Actor1Geo_Long, DATEADDED',
            'startIndex': index,
            'maxResults': 50
        }
        response = requests.get(
            self.endpoint,
            headers=header,
            params=params,
            verify=False)

        if response.status_code != 200:
            error_message = "Was unable to retrieve GDELT data"
            raise SystemError(error_message)
            logger.error(error_message)

        body = json.loads(response.text)
        if "pageToken" not in body:
            index = int(body['totalRows']) - 1
            fb = Firebase()
            fb.update_index(index)
        acquired_data = body['rows']
        return acquired_data

    def get_access_token(self):
        data = {'client_id': self.google_client_id,
                'client_secret': self.google_client_secret,
                'refresh_token': self.refresh_token,
                'grant_type': 'refresh_token'}
        response = requests.post(self.google_auth_url, data=data)
        if response.status_code != 200:
            error_message = "Unable to get Access Token from Google API"
            raise SystemError(error_message)
            logger.error(error_message)

        response_body = json.loads(response.text)
        return response_body['access_token']

    def get_row_count(self):
        auth_token = self.get_access_token()
        header = {'Authorization': 'Bearer ' + auth_token}
        params = {
            'maxResults': 1
        }
        response = requests.get(
            self.endpoint,
            headers=header,
            params=params,
            verify=False)

        if response.status_code != 200:
            error_message = "Was unable to retrieve GDELT data"
            raise SystemError(error_message)
            logger.error(error_message)

        body = json.loads(response.text)
        if "totalRows" in body:
            row_count = body['totalRows']
        else:
            row_count = None
        return int(row_count)


def api_data_mapper(row):
    try:
        date_added = row[5]['v']
        tone = row[2]['v']
        goldstein = row[1]['v']
        actor_code = row[0]['v']
        lat = row[3]['v']
        lon = row[4]['v']
        adjusted_date_added = datetime.datetime.strptime(date_added, "%Y%m%d%H%M%S")
        data = {
            'avg_tone': tone if tone is not None else '',
            'goldstein': goldstein if goldstein is not None else '',
            'actor_code': actor_code if actor_code is not None else '',
            'lat': lat if lat is not None else '',
            'lon': lon if lon is not None else '',
            'date': str(adjusted_date_added)
        }
        return data
    except TypeError as e:
        logger.error(f"Error during mapping the data to a Domino Data Lab API required form: {e}")
    except ValueError as e:
        logger.error(f"Error during mapping the data to a Domino Data Lab API required form: {e}")


def post_data(data):
    basic_auth_key = '58BTaPnrmzIDtI0VrVVz6v6qKOu8ABmYZzDGhTmaoW7xgddOhx9ISGdAndVVdziE'
    endpoint = 'https://app-models.dominodatalab.com:443/models/5bd0856346e0fb0008d06d74/latest/model'
    body = {'data': data}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        endpoint,
        data=json.dumps(body),
        headers=headers,
        auth=(basic_auth_key, basic_auth_key),
        verify=False)

    if response.status_code != 200:
        logger.error(f"Unable to add data to Domino Data Lab for actor {data['actor_code']}, {data['date']}")
        return None
    response_body = json.loads(response.text)
    return response_body


def database_data_mapper(data, api_response):
    try:
        mapped_data = {
            'id': api_response['request_id'],
            'timing': api_response['timing'],
            'class1': api_response['result']['class1'],
            'class2': api_response['result']['class2'],
            'average_tone': float(data['avg_tone']),
            'goldstein': float(data['goldstein']),
            'latitude': data['lat'],
            'longitude': data['lon']
        }
        return mapped_data
    except TypeError as e:
        logger.error(f"Error during mapping the data to a Cosmos friendly form: {e}")
    except ValueError as e:
        logger.error(f"Error during mapping the data to a Cosmos friendly form: {e}")


def add_data_to_database(data):
    try:
        fb = Firebase()
        fb.add_document(data, data['id'])
    except Exception as e:
        logger.error(f"Error during adding the data to Cosmos: {e}")


def handler():
    fb = Firebase()
    index = fb.get_index()

    google_service = GoogleBigQuery()
    row_count = google_service.get_row_count()
    while row_count > index + 1:
        rows = google_service.get_gdelt_data(index)
        for row in rows:
            #todo: make this async. celery if have time.
            data = api_data_mapper(row['f'])
            api_response = post_data(data)
            if api_response is not None:
                mapped_data = database_data_mapper(data, api_response)
                add_data_to_database(mapped_data)
        index = index + 50
