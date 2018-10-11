from tornado.web import RequestHandler
from tornado.httpclient import HTTPClient
import urllib

from settings import (
    SPOTIFY_AUTHORIZE_URL,
    SPOTIFY_TOKEN_URL,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
)


class LoginHandler(RequestHandler):

    def get(self):
        query_parameters = {
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': 'http://localhost:8080/callback',
            # 'scopes': 'user-top-read',
        }
        spotify_authorize_url = '{base}?{query_string}'.format(
            base=SPOTIFY_AUTHORIZE_URL,
            query_string=urllib.urlencode(query_parameters),
        )

        self.redirect(spotify_authorize_url, permanent=True)


class SpotifyAuthorizeCallbackHandler(RequestHandler):

    def get(self):
        authorization_code = self.get_argument('code')
        post_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': 'http://localhost:8080/callback',
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
        }
        body = urllib.urlencode(post_data)
        http_client = HTTPClient()
        response = http_client.fetch(
            SPOTIFY_TOKEN_URL,
            method='POST',
            body=body
        )

        self.write(response.body)
