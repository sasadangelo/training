from access_token import AuthData, AccessToken
from athlete import Athlete
from stravaio import StravaIO

auth_data = AuthData(
    endpoint='https://www.strava.com/api/v3/oauth/token',
    client_id='105956',
    client_secret='f86d32922372d893fd6868b2f31b76f098b5229e',
    refresh_token='a87cf44fb1798360a75d750ba8b2286d59957c6d'
)

access_token = AccessToken(auth_data=auth_data).get_access_token()
print(access_token)
client = StravaIO(access_token=access_token)

#activities = client.get_logged_in_athlete_activities()
athlete = client.get_logged_in_athlete()
my_athlete = Athlete(
    firstname=athlete.api_response.firstname,
    lastname=athlete.api_response.lastname,
    city=athlete.api_response.city,
    state=athlete.api_response.state,
    country=athlete.api_response.country,
    sex=athlete.api_response.sex
)

print(my_athlete)
