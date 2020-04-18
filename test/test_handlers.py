import json
from unittest.mock import patch
from urllib import parse

import server
import vcr
from tornado.testing import AsyncHTTPTestCase


class StatusHandlerTest(AsyncHTTPTestCase):
    def get_app(self):
        return server.make_app()

    def test_get(self):
        response = self.fetch(path="/status", method="GET")

        # Verify the response code.
        self.assertEqual(response.code, 200)

        # Verify response body.
        parsed_response = json.loads(response.body)
        self.assertDictEqual(parsed_response, {"message": "ok", "status": 200})


class IndexHandlerTest(AsyncHTTPTestCase):
    def get_app(self):
        return server.make_app()

    @vcr.use_cassette(
        "test/cassettes/index_handler_test/test_get.yml", ignore_localhost=True,
    )
    @patch(
        "musictaxonomy.handlers.BaseAPIHandler.get_secure_cookie",
        return_value="test_access_token".encode(),
    )
    def test_get(self, _):
        headers = {"Cookie": "AccessToken=test_access_token"}
        response = self.fetch(path="/", headers=headers, method="GET")

        # Verify the response code.
        self.assertEqual(response.code, 200)

    def test_get_without_access_token(self):
        response = self.fetch(path="/", method="GET", follow_redirects=False)

        # Verify the response code.
        self.assertEqual(response.code, 302)

        # Verify the redirect host and path.
        parsed_url = parse.urlparse(response.headers["Location"])
        self.assertEqual(parsed_url.netloc, "")
        self.assertEqual(parsed_url.path, "/login")
