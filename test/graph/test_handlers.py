import json

import vcr
from jsonschema import validate
from tornado.testing import AsyncHTTPTestCase

import server


class TaxonomyGraphHandlerTest(AsyncHTTPTestCase):

    def get_app(self):
        return server.make_app()

    @vcr.use_cassette(
        'test/graph/cassettes/taxonomy_graph_handler_test/test_get.yml',
        ignore_localhost=True
    )
    def test_get(self):
        headers = {
            "Cookie": "AccessToken=2|1:0|10:1557112070|11:AccessToken|208:QlFERHdTaF9FTmJPMn"
                      "Z0T1A2bEg2Z0Mtdjk4QzZndjdZV1RBZERZcFp1TTM5SlNmVVBkV2RybGFuX1JoQW1fZlZ"
                      "HajV0djR3dE5fbkxzNjNMRVBvZ2ttRjNEY1dJUmpHNVJzV1VEUTRlVjVKS0lVQV9fSlNO"
                      "S0dpVU9GbHFpdHFYSHgyRHhnN2VRNlduXzN5S1RoZ2RpSk5IeHR2|d960f7c5da188ca1"
                      "3c0e1307e9c91fe81ea9d877308acc90da076738143b70c5",
        }
        response = self.fetch(
            path='/taxonomy_graphs',
            method='GET',
            headers=headers,
            follow_redirects=False,
        )

        # Verify the response code.
        self.assertEqual(response.code, 200)

        # Verify response body.
        parsed_response = json.loads(response.body)
        schema = {
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "color": {"type": "string"},
                            "source": {"type": "string"},
                            "target": {"type": "string"},
                        },
                    },
                },
                "links": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "color": {"type": "string"},
                            "fontSize": {"type": "number"},
                            "name": {"type": "string"},
                            "size": {"type": "number"},
                            "id": {"type": "string"},
                            "strokeColor": {"type": "string"},
                        },
                    },
                },
            },
        }
        validate(instance=parsed_response, schema=schema)

    def test_get_without_access_token(self):
        response = self.fetch(
            path='/taxonomy_graphs',
            method='GET',
            follow_redirects=False,
        )

        # Verify the response code.
        self.assertEqual(response.code, 401)

        # Verify response body.
        parsed_response = json.loads(response.body)
        self.assertDictEqual(
            parsed_response,
            {'error': {'code': 401, 'message': 'Unauthorized'}}
        )
