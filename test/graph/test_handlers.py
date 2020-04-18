import json
from unittest.mock import patch

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
    @patch(
        "musictaxonomy.handlers.BaseAPIHandler.get_secure_cookie",
        return_value="test_access_token".encode(),
    )
    def test_get(self, _):
        headers = {"Cookie": "test_access_token"}
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
