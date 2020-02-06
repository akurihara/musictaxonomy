import json
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
        "test/cassettes/index_handler_test/test_get.yml", ignore_localhost=True
    )
    def test_get(self):
        headers = {
            "Cookie": "AccessToken=2|1:0|10:1580964418|11:AccessToken|208:QlFDUnpBQXBXbTQyV1JyWT"
            "V5dUtnWm50WmFGbWVwTnFETXJfbGxoUVNNVlplZ2lVb3RZdm0xU0Z2cUU3VEhDYjlyajM0dGJuX0NBLTZDX"
            "zlRRGxCcHVYNlNfVGM2Qkd5OUl2Q1ExdThtRVc0aUdDUUZuZUdLczEyNDFNcWNqS0hFN3VxYnhtcnlFZExa"
            "SWFiX0N0QmdpdjRsdw==|d355ece9d278c7fbce2219da0c8567be0eb31fc40f16147195062fc2a183b391"
        }
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
