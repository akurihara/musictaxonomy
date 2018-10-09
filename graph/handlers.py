import json

from tornado.web import RequestHandler

from example_response import LONG_TERM_ARTISTS
from graph import service as graph_service


class GraphExampleHandler(RequestHandler):

    def get(self):
        artists = graph_service.parse_artists_from_spotify_response(json.loads(LONG_TERM_ARTISTS))
        taxonomy_graph = graph_service.build_taxonomy_graph_from_artists(artists)

        response_lines = []
        for node in taxonomy_graph:
            for neighbor in node.get_neighbors():
                response_lines.append('  "{}" -> "{}"'.format(node.id, neighbor.id))

        response = '\n'.join(response_lines)
        self.write(response)
