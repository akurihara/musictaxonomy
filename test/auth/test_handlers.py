import json
from urllib.parse import parse_qsl, urlparse

from tornado.testing import AsyncHTTPTestCase

import server
from settings import HOST, SPOTIFY_CLIENT_ID


class LoginHandlerTest(AsyncHTTPTestCase):

    def get_app(self):
        return server.make_app()

    def test_get(self):
        response = self.fetch(
            path='/login',
            method='GET',
            follow_redirects=False,
        )

        self.assertEqual(response.code, 302)
        parsed_url = urlparse(response.headers['Location'])
        self.assertEqual(parsed_url.netloc, 'accounts.spotify.com')
        self.assertEqual(parsed_url.path, '/authorize')
        parsed_query_string = dict(parse_qsl(parsed_url.query))
        self.assertEqual(parsed_query_string['response_type'], 'code')
        self.assertEqual(parsed_query_string['scope'], 'user-top-read')
        self.assertEqual(parsed_query_string['client_id'], SPOTIFY_CLIENT_ID)
        self.assertEqual(parsed_query_string['redirect_uri'], '{}/callback/oauth'.format(HOST))


class OauthCallbackHandlerTest(AsyncHTTPTestCase):

    def get_app(self):
        return server.make_app()

    def test_get(self):
        pass
