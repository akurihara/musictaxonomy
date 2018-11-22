import json

from tornado.httpclient import AsyncHTTPClient
import urllib.parse

from settings import SPOTIFY_API_BASE_URL


async def get_all_top_artists_for_user(access_token):
    return await _get_top_artists_in_time_range(access_token)


async def _get_top_artists_in_time_range(access_token, time_range='medium_term', limit=50):
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
