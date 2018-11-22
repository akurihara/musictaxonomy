from __future__ import absolute_import
import json

from tornado.httpclient import AsyncHTTPClient
import urllib.parse

from auth.models import SpotifyAuthorization
from database_utils import Session
from handlers import BaseAPIHandler
from settings import (
    SPOTIFY_AUTHORIZE_URL,
    SPOTIFY_TOKEN_URL,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
)


class LoginHandler(BaseAPIHandler):

    def get(self):
        access_token = self.get_cookie('AccessToken')
        if access_token:
            self.write('Already logged in')
            return

        query_parameters = {
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': 'http://localhost:8080/callback/oauth',
            # 'scopes': 'user-top-read',
        }
        spotify_authorize_url = '{base}?{query_string}'.format(
            base=SPOTIFY_AUTHORIZE_URL,
            query_string=urllib.parse.urlencode(query_parameters),
        )

        return self.redirect(spotify_authorize_url, permanent=False)


class OauthCallbackHandler(BaseAPIHandler):

    async def get(self):
        authorization_code = self.get_argument('code')
        post_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': 'http://localhost:8080/callback/oauth',
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
        }
        body = urllib.parse.urlencode(post_data)
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(
            SPOTIFY_TOKEN_URL,
            method='POST',
            body=body
        )

        parsed_response = json.loads(response.body)
        access_token = parsed_response['access_token']
        refresh_token = parsed_response['refresh_token']

        spotify_authorization = SpotifyAuthorization(
            access_token=access_token,
            refresh_token=refresh_token,
        )
        session = Session()
        session.add(spotify_authorization)
        session.commit()

        self.set_cookie('AccessToken', access_token)

        return self.write({'success': True})
