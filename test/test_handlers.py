import json
from urllib import parse

import vcr
from tornado.testing import AsyncHTTPTestCase

import server


class StatusHandlerTest(AsyncHTTPTestCase):

    def get_app(self):
        return server.make_app()

    def test_get(self):
        response = self.fetch(
            path='/status',
            method='GET',
        )

        # Verify the response code.
        self.assertEqual(response.code, 200)

        # Verify response body.
        parsed_response = json.loads(response.body)
        self.assertDictEqual(parsed_response, {'message': 'ok', 'status': 200})


class IndexHandlerTest(AsyncHTTPTestCase):

    def get_app(self):
        return server.make_app()

    @vcr.use_cassette('test/cassettes/index_handler_test/test_get.yml', ignore_localhost=True)
    def test_get(self):
        headers = {
            "Cookie": "AccessToken=2|1:0|10:1557112070|11:AccessToken|208:QlFERHdTaF9FTmJPMn"
                      "Z0T1A2bEg2Z0Mtdjk4QzZndjdZV1RBZERZcFp1TTM5SlNmVVBkV2RybGFuX1JoQW1fZlZ"
                      "HajV0djR3dE5fbkxzNjNMRVBvZ2ttRjNEY1dJUmpHNVJzV1VEUTRlVjVKS0lVQV9fSlNO"
                      "S0dpVU9GbHFpdHFYSHgyRHhnN2VRNlduXzN5S1RoZ2RpSk5IeHR2|d960f7c5da188ca1"
                      "3c0e1307e9c91fe81ea9d877308acc90da076738143b70c5",
        }
        response = self.fetch(
            path='/',
            headers=headers,
            method='GET',
        )

        # Verify the response code.
        self.assertEqual(response.code, 200)

    def test_get_without_access_token(self):
        response = self.fetch(
            path='/',
            method='GET',
            follow_redirects=False,
        )

        # Verify the response code.
        self.assertEqual(response.code, 302)

        # Verify the redirect host and path.
        parsed_url = parse.urlparse(response.headers['Location'])
        self.assertEqual(parsed_url.netloc, '')
        self.assertEqual(parsed_url.path, '/login')
