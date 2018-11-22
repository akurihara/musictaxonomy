from __future__ import absolute_import
import json

from tornado.web import HTTPError

from example_response import LONG_TERM_ARTISTS
from graph import service as graph_service
from handlers import BaseAPIHandler


class TaxonomyGraphExampleHandler(BaseAPIHandler):

    def get(self):
        artists = graph_service.parse_artists_from_spotify_response(json.loads(LONG_TERM_ARTISTS))
        taxonomy_graph = graph_service.build_taxonomy_graph_from_artists(artists)

        response_lines = []
        for node in taxonomy_graph:
            for neighbor in node.get_neighbors():
                response_lines.append('  "{}" -> "{}"'.format(node.id, neighbor.id))

        response = '\n'.join(response_lines)
        return self.write(response)


class CreateTaxonomyGraphHandler(BaseAPIHandler):

    def get(self):
        return self.write('hello')

    def post(self):
        print('** hello')
        access_token = self.get_cookie('AccessToken')
        print(access_token)
        raise HTTPError(reason='Must be logged in.')
