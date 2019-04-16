import json

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
        response_body = json.loads(response.body)

        expected_response = {
            'message': 'ok',
            'status': 200,
        }
        self.assertEqual(response.code, 200)
        self.assertEqual(response_body, expected_response)
