from __future__ import absolute_import
import json

from tornado.web import HTTPError

from example_response import LONG_TERM_ARTISTS
from graph import service as graph_service
from handlers import BaseAPIHandler
from spotify import client as spotify_client


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

    async def get(self):
        access_token = self.get_cookie('AccessToken')

        if not access_token:
            raise HTTPError(status_code=401)

        response = await spotify_client.get_all_top_artists_for_user(access_token)
        artists = graph_service.parse_artists_from_spotify_response(response)
        taxonomy_graph = graph_service.build_taxonomy_graph_from_artists(artists)
        response = taxonomy_graph.render_in_webgraphviz_format()

        return self.write(response)
