import json

from tornado.httpclient import AsyncHTTPClient
import urllib.parse

from musictaxonomy.spotify import constants as spotify_constants
from settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


__all__ = [
    'get_access_token',
    'get_current_user_profile',
    'get_top_artists_in_time_range',
]


async def get_access_token(authorization_code: str, redirect_base_url: str):
    post_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': '{}/callback/oauth'.format(redirect_base_url),
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }
    body = urllib.parse.urlencode(post_data)
    response = await AsyncHTTPClient().fetch(
        spotify_constants.SPOTIFY_TOKEN_URL,
        method='POST',
        body=body
    )

    return json.loads(response.body)


async def get_current_user_profile(access_token: str):
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    url = '{base}/me'.format(base=spotify_constants.SPOTIFY_API_BASE_URL)

    response = await AsyncHTTPClient().fetch(
        url,
        method='GET',
        headers=headers,
    )

    parsed_body = json.loads(response.body)

    return parsed_body


async def get_top_artists_in_time_range(access_token: str, time_range: str):
    query_parameters = {
        'time_range': time_range,
        'limit': 50,
    }
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    url = '{base}/me/top/artists?{query_string}'.format(
        base=spotify_constants.SPOTIFY_API_BASE_URL,
        query_string=urllib.parse.urlencode(query_parameters),
    )

    response = await AsyncHTTPClient().fetch(
        url,
        method='GET',
        headers=headers,
    )

    parsed_body = json.loads(response.body)

    return parsed_body
