from typing import Tuple
import pickle
import requests
import datetime
import time
from stravaio import StravaIO

class AuthData:
    def __init__(self, endpoint: str, client_id: str, client_secret: str, refresh_token: str):
        self.endpoint = endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

class AccessToken:
    def __init__(self, auth_data: AuthData):
        self.auth_data = auth_data
        self.token_cache = {}
    
    def _put_access_token_to_cache(self, access_token: str, expires_at: int) -> None:
        print("_put_access_token_to_cache")
        data = {
            "access_token": access_token,
            "expires_at": expires_at
        }
        with open("strava_cache.pkl", "wb") as f:
            pickle.dump(data, f)
    
    def _get_access_token_from_cache(self) -> Tuple[str, int]:
        print("_get_access_token_from_cache")
        try:
            with open("strava_cache.pkl", "rb") as f:
                data = pickle.load(f)
                if data["expires_at"] > time.time():
                    return data["access_token"], data["expires_at"]
        except FileNotFoundError:
            pass
        return None, None
    
    def _refresh_access_token(self) -> Tuple[str, int]:
        print("_refresh_access_token")
        payload = {
            "client_id": self.auth_data.client_id,
            'client_secret': self.auth_data.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.auth_data.refresh_token,
        }
        response = requests.post(self.auth_data.endpoint, data=payload)
        if response.status_code != 200:
            raise Exception('Failed to refresh access token')

        # Extract the new access token and its expiration time
        access_token = response.json()['access_token']
        expires_at = response.json()['expires_at']

        # Return the new access token and its expiration time as a tuple
        return access_token, expires_at
    
    def get_access_token(self) -> str:
        print("get_access_token")
        access_token, expiration_time = self._get_access_token_from_cache()
        if access_token is not None and datetime.datetime.now().timestamp() < expiration_time:
            return access_token
        else:
            access_token, expires_at = self._refresh_access_token()
            self._put_access_token_to_cache(access_token, expires_at)
            return access_token
