from tornado.web import HTTPError

from database_utils import Session
from graph import service as graph_service
from handlers import BaseAPIHandler
from spotify import service as spotify_service


class CreateTaxonomyGraphHandler(BaseAPIHandler):

    async def get(self):
        access_token = self.get_cookie('AccessToken')

        if not access_token:
            raise HTTPError(status_code=401)

        spotify_artists = await spotify_service.get_all_top_artists_for_user(access_token)
        session = Session()
        taxonomy_graph = graph_service.build_taxonomy_graph_from_spotify_artists(session, spotify_artists)

        # response = taxonomy_graph.render_in_webgraphviz_format()
        response = taxonomy_graph.render_as_json()

        return self.write(response)
