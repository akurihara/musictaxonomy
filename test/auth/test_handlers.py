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
    def test_get_with_valid_access_token(self):
        headers = {
            "Cookie": "AccessToken=2|1:0|10:1580964418|11:AccessToken|208:QlFDUnpBQXBXbTQyV1JyWT"
            "V5dUtnWm50WmFGbWVwTnFETXJfbGxoUVNNVlplZ2lVb3RZdm0xU0Z2cUU3VEhDYjlyajM0dGJuX0NBLTZDX"
            "zlRRGxCcHVYNlNfVGM2Qkd5OUl2Q1ExdThtRVc0aUdDUUZuZUdLczEyNDFNcWNqS0hFN3VxYnhtcnlFZExa"
            "SWFiX0N0QmdpdjRsdw==|d355ece9d278c7fbce2219da0c8567be0eb31fc40f16147195062fc2a183b391"
        }
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
    def test_get_with_invalid_access_token(self):
        headers = {
            "Cookie": "AccessToken=2|1:0|10:1580964418|11:AccessToken|208:QlFDUnpBQXBXbTQyV1JyWT"
            "V5dUtnWm50WmFGbWVwTnFETXJfbGxoUVNNVlplZ2lVb3RZdm0xU0Z2cUU3VEhDYjlyajM0dGJuX0NBLTZDX"
            "zlRRGxCcHVYNlNfVGM2Qkd5OUl2Q1ExdThtRVc0aUdDUUZuZUdLczEyNDFNcWNqS0hFN3VxYnhtcnlFZExa"
            "SWFiX0N0QmdpdjRsdw==|d355ece9d278c7fbce2219da0c8567be0eb31fc40f16147195062fc2a183b391"
        }
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
