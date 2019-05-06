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

    def test_get_without_access_token(self):
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

    @vcr.use_cassette('test/auth/cassettes/test_get_with_valid_access_token.yml', ignore_localhost=True)
    def test_get_with_valid_access_token(self):
        headers = {
            "Cookie": "AccessToken=2|1:0|10:1557112070|11:AccessToken|208:QlFERHdTaF9FTmJPMn"
                      "Z0T1A2bEg2Z0Mtdjk4QzZndjdZV1RBZERZcFp1TTM5SlNmVVBkV2RybGFuX1JoQW1fZlZ"
                      "HajV0djR3dE5fbkxzNjNMRVBvZ2ttRjNEY1dJUmpHNVJzV1VEUTRlVjVKS0lVQV9fSlNO"
                      "S0dpVU9GbHFpdHFYSHgyRHhnN2VRNlduXzN5S1RoZ2RpSk5IeHR2|d960f7c5da188ca1"
                      "3c0e1307e9c91fe81ea9d877308acc90da076738143b70c5",
        }
        response = self.fetch(
            path='/login',
            method='GET',
            headers=headers,
            follow_redirects=False,
        )

        # Verify the response code.
        self.assertEqual(response.code, 302)

        # Verify the redirect host and path.
        parsed_url = parse.urlparse(response.headers['Location'])
        self.assertEqual(parsed_url.netloc, '')
        self.assertEqual(parsed_url.path, '/')

    @vcr.use_cassette('test/auth/cassettes/test_get_with_invalid_access_token.yml', ignore_localhost=True)
    def test_get_with_invalid_access_token(self):
        headers = {
            "Cookie": "AccessToken=invalid",
        }
        response = self.fetch(
            path='/login',
            method='GET',
            headers=headers,
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

    @vcr.use_cassette('test/auth/cassettes/test_get_with_existing_user.yml', ignore_localhost=True)
    def test_get_with_existing_user(self):
        # Create a user in the database.
        user = User(
            display_name='Alex Kurihara',
            external_id=1220628328,
            external_source='spotify',
        )
        self.session.add(user)
        self.session.commit()
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

        # Verify a new user was not created in the database.
        self.assertEqual(self.session.query(User).count(), 1)
