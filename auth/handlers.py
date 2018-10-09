from tornado.web import RequestHandler
import urllib

from settings import SPOTIFY_AUTHORIZE_BASE_URL, SPOTIFY_CLIENT_ID


class LoginHandler(RequestHandler):

    def get(self):
        query_parameters = {
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': 'localhost:8888/callback',
            'scopes': 'user-top-read',
        }
        spotify_authorize_url = '{base}?{query_string}'.format(
            base=SPOTIFY_AUTHORIZE_BASE_URL,
            query_string=urllib.urlencode(query_parameters),
        )

        self.redirect(spotify_authorize_url, permanent=True)
