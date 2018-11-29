import json

from tornado.httpclient import AsyncHTTPClient
import urllib.parse

from settings import (
    SPOTIFY_API_BASE_URL,
    SPOTIFY_TOKEN_URL,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
)


__all__ = [
    'request_access_token',
    'get_all_top_artists_for_user',
]


async def request_access_token(authorization_code: str):
    post_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': 'http://localhost:8080/callback/oauth',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }
    body = urllib.parse.urlencode(post_data)
    response = await AsyncHTTPClient().fetch(
        SPOTIFY_TOKEN_URL,
        method='POST',
        body=body
    )

    return json.loads(response.body)


async def get_all_top_artists_for_user(access_token: str):
    return await _get_top_artists_in_time_range(access_token)


async def _get_top_artists_in_time_range(access_token: str, time_range='medium_term', limit=50):
    query_parameters = {
        'time_range': time_range,
        'limit': limit,
    }
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    url = '{base}/me/top/artists?{query_string}'.format(
        base=SPOTIFY_API_BASE_URL,
        query_string=urllib.parse.urlencode(query_parameters),
    )
    response = await AsyncHTTPClient().fetch(
        url,
        method='GET',
        headers=headers,
    )

    parsed_body = json.loads(response.body)

    return parsed_body