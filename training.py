from typing import Tuple
import pickle
from stravaio import StravaIO
import pandas as pd
from sqlalchemy import create_engine
import requests
import datetime
import time

TOKEN_CACHE = {}
TOKEN_ENDPOINT = 'https://www.strava.com/api/v3/oauth/token'
CLIENT_ID = '105956'
CLIENT_SECRET = 'f86d32922372d893fd6868b2f31b76f098b5229e'
REFRESH_TOKEN = 'a87cf44fb1798360a75d750ba8b2286d59957c6d'

# This is the token cache that will be renewed every time it expires
TOKEN_CACHE = {}

def put_access_token_to_cache(access_token, expires_at):
    data = {
        "access_token": access_token,
        "expires_at": expires_at
    }
    with open("strava_cache.pkl", "wb") as f:
        pickle.dump(data, f)

def get_access_token_from_cache():
    try:
        with open("strava_cache.pkl", "rb") as f:
            data = pickle.load(f)
            if data["expires_at"] > time.time():
                return data["access_token"], data["expires_at"]
    except FileNotFoundError:
        pass
    return None, None

def refresh_access_token() -> Tuple[str, int]:
    payload = {
        "client_id": CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
    }
    response = requests.post(TOKEN_ENDPOINT, data=payload)
    if response.status_code != 200:
        raise Exception('Failed to refresh access token')

    # Extract the new access token and its expiration time
    access_token = response.json()['access_token']
    expires_at = response.json()['expires_at']

    # Return the new access token and its expiration time as a tuple
    return access_token, expires_at

def get_access_token():
    access_token, expiration_time = get_access_token_from_cache()
    if access_token is not None and datetime.datetime.now() < expiration_time:
        return access_token
    else:
        access_token, expires_at = refresh_access_token()
        put_access_token_to_cache(access_token, expires_at)
        return access_token

access_token = get_access_token()
print(access_token)
client = StravaIO(access_token=access_token)

activities = client.get_logged_in_athlete_activities()

for activity in activities:
    print(activity)
