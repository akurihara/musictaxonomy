from unittest.mock import patch
from urllib import parse

import server
import vcr
from musictaxonomy.auth.models import User
from musictaxonomy.database import Session
from settings import SPOTIFY_CLIENT_ID
from tornado.testing import AsyncHTTPTestCase


class LoginHandlerTest(AsyncHTTPTestCase):
    def get_app(self):
        return server.make_app()

    def test_get_without_access_token(self):
        response = self.fetch(path="/login", method="GET", follow_redirects=False)

        # Verify the response code.
        self.assertEqual(response.code, 302)

        # Verify the redirect host and path.
        parsed_url = parse.urlparse(response.headers["Location"])
        self.assertEqual(parsed_url.netloc, "accounts.spotify.com")
        self.assertEqual(parsed_url.path, "/authorize")

        # Verify the redirect query parameters.
        parsed_query_string = dict(parse.parse_qsl(parsed_url.query))
        self.assertEqual(parsed_query_string["response_type"], "code")
        self.assertEqual(parsed_query_string["scope"], "user-top-read")
        self.assertEqual(parsed_query_string["client_id"], SPOTIFY_CLIENT_ID)
        self.assertTrue(parsed_query_string["redirect_uri"].endswith("/callback/oauth"))

    @vcr.use_cassette(
        "test/auth/cassettes/login_handler_test/test_get_with_valid_access_token.yml",
        ignore_localhost=True,
    )
    @patch(
        "musictaxonomy.handlers.BaseAPIHandler.get_secure_cookie",
        return_value="test_access_token".encode(),
    )
    def test_get_with_valid_access_token(self, _):
        headers = {"Cookie": "test_access_token"}
        response = self.fetch(
            path="/login", method="GET", headers=headers, follow_redirects=False
        )

        # Verify the response code.
        self.assertEqual(response.code, 302)

        # Verify the redirect host and path.
        parsed_url = parse.urlparse(response.headers["Location"])
        self.assertEqual(parsed_url.netloc, "")
        self.assertEqual(parsed_url.path, "/")

    @vcr.use_cassette(
        "test/auth/cassettes/login_handler_test/test_get_with_invalid_access_token.yml",
        ignore_localhost=True,
    )
    @patch(
        "musictaxonomy.handlers.BaseAPIHandler.get_secure_cookie",
        return_value="invalid_access_token".encode(),
    )
    def test_get_with_invalid_access_token(self, _):
        headers = {"Cookie": "AccessToken=invalid_access_token"}
        response = self.fetch(
            path="/login", method="GET", headers=headers, follow_redirects=False
        )

        # Verify the response code.
        self.assertEqual(response.code, 302)

        # Verify the redirect host and path.
        parsed_url = parse.urlparse(response.headers["Location"])
        self.assertEqual(parsed_url.netloc, "accounts.spotify.com")
        self.assertEqual(parsed_url.path, "/authorize")

        # Verify the redirect query parameters.
        parsed_query_string = dict(parse.parse_qsl(parsed_url.query))
        self.assertEqual(parsed_query_string["response_type"], "code")
        self.assertEqual(parsed_query_string["scope"], "user-top-read")
        self.assertEqual(parsed_query_string["client_id"], SPOTIFY_CLIENT_ID)
        self.assertTrue(parsed_query_string["redirect_uri"].endswith("/callback/oauth"))


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

    @vcr.use_cassette(
        "test/auth/cassettes/oauth_callback_handler_test/test_get_with_new_user.yml",
        ignore_localhost=True,
    )
    def test_get_with_new_user(self):
        query_parameters = {"code": "AQAYIHUkyhPGAtmQ"}
        url = "{}?{}".format("/callback/oauth", parse.urlencode(query_parameters))

        response = self.fetch(path=url, method="GET", follow_redirects=False)

        # Verify the response code.
        self.assertEqual(response.code, 302)

        # Verify the redirect host and path.
        parsed_url = parse.urlparse(response.headers["Location"])
        self.assertEqual(parsed_url.netloc, "")
        self.assertEqual(parsed_url.path, "/")

        # Verify a new user was created in the database.
        user = self.session.query(User).filter_by(external_id=1220628328).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.display_name, "Alex Kurihara")
        self.assertEqual(user.external_source, "spotify")

    @vcr.use_cassette(
        "test/auth/cassettes/oauth_callback_handler_test/test_get_with_existing_user.yml",
        ignore_localhost=True,
    )
    def test_get_with_existing_user(self):
        # Create a user in the database.
        user = User(
            display_name="Alex Kurihara",
            external_id=1220628328,
            external_source="spotify",
        )
        self.session.add(user)
        self.session.commit()
        query_parameters = {"code": "AQAYIHUkyhPGAtmQ"}
        url = "{}?{}".format("/callback/oauth", parse.urlencode(query_parameters))

        response = self.fetch(path=url, method="GET", follow_redirects=False)

        # Verify the response code.
        self.assertEqual(response.code, 302)

        # Verify the redirect host and path.
        parsed_url = parse.urlparse(response.headers["Location"])
        self.assertEqual(parsed_url.netloc, "")
        self.assertEqual(parsed_url.path, "/")

        # Verify a new user was not created in the database.
        self.assertEqual(self.session.query(User).count(), 1)
