import json

import server
import vcr
from jsonschema import validate
from tornado.testing import AsyncHTTPTestCase


class TaxonomyGraphHandlerTest(AsyncHTTPTestCase):
    def get_app(self):
        return server.make_app()

    @vcr.use_cassette(
        "test/graph/cassettes/taxonomy_graph_handler_test/test_get.yml",
        ignore_localhost=True,
    )
    def test_get(self):
        headers = {
            "Cookie": "AccessToken=2|1:0|10:1580964418|11:AccessToken|208:QlFDUnpBQXBXbTQyV1JyWT"
            "V5dUtnWm50WmFGbWVwTnFETXJfbGxoUVNNVlplZ2lVb3RZdm0xU0Z2cUU3VEhDYjlyajM0dGJuX0NBLTZDX"
            "zlRRGxCcHVYNlNfVGM2Qkd5OUl2Q1ExdThtRVc0aUdDUUZuZUdLczEyNDFNcWNqS0hFN3VxYnhtcnlFZExa"
            "SWFiX0N0QmdpdjRsdw==|d355ece9d278c7fbce2219da0c8567be0eb31fc40f16147195062fc2a183b391"
        }
        response = self.fetch(
            path="/taxonomy_graphs",
            method="GET",
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
            path="/taxonomy_graphs", method="GET", follow_redirects=False
        )

        # Verify the response code.
        self.assertEqual(response.code, 401)

        # Verify response body.
        parsed_response = json.loads(response.body)
        self.assertDictEqual(
            parsed_response, {"error": {"code": 401, "message": "Unauthorized"}}
        )
