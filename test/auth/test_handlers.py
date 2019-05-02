from urllib import parse
from tornado.testing import AsyncHTTPTestCase

import vcr

import server
from musictaxonomy.auth.models import User
from musictaxonomy.database import Session
from settings import SPOTIFY_CLIENT_ID


class LoginHandlerTest(AsyncHTTPTestCase):

    def get_app(self):
        return server.make_app()

    def test_get(self):
        response = self.fetch(
            path='/login',
            method='GET',
            follow_redirects=False,
        )

        # Verify the response code.
        self.assertEqual(response.code, 302)

        # Verify the redirect host and path.
        parsed_url = parse.urlparse(response.headers['Location'])
        self.assertEqual(parsed_url.netloc, 'accounts.spotify.com')
        self.assertEqual(parsed_url.path, '/authorize')

        # Verify the redirect query parameters.
        parsed_query_string = dict(parse.parse_qsl(parsed_url.query))
        self.assertEqual(parsed_query_string['response_type'], 'code')
        self.assertEqual(parsed_query_string['scope'], 'user-top-read')
        self.assertEqual(parsed_query_string['client_id'], SPOTIFY_CLIENT_ID)
        self.assertTrue(parsed_query_string['redirect_uri'].endswith('/callback/oauth'))


class OauthCallbackHandlerTest(AsyncHTTPTestCase):

    def setUp(self):
        super().setUp()
        self.session = Session()

    def tearDown(self):
        super().tearDown()
        self.session.query(User).delete()
        self.session.commit()

    def get_app(self):
        return server.make_app()

    @vcr.use_cassette('test/auth/cassettes/test_get_with_new_user.yml', ignore_localhost=True)
    def test_get_with_new_user(self):
        query_parameters = {
            'code': 'AQAYIHUkyhPGAtmQ'
        }
        url = '{}?{}'.format('/callback/oauth', parse.urlencode(query_parameters))

        response = self.fetch(
            path=url,
            method='GET',
            follow_redirects=False,
        )

        # Verify the response code.
        self.assertEqual(response.code, 302)

        # Verify the redirect host and path.
        parsed_url = parse.urlparse(response.headers['Location'])
        self.assertEqual(parsed_url.netloc, '')
        self.assertEqual(parsed_url.path, '/')

        # Verify a new user was created in the database.
        user = self.session.query(User).filter_by(external_id=1220628328).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.display_name, 'Alex Kurihara')
        self.assertEqual(user.external_source, 'spotify')
