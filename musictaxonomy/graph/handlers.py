from tornado.web import HTTPError

from musictaxonomy.database import Session
from musictaxonomy.graph import service as graph_service
from musictaxonomy.handlers import BaseAPIHandler
from musictaxonomy.spotify import service as spotify_service


class TaxonomyGraphHandler(BaseAPIHandler):

    async def get(self):
        access_token = self.get_access_token()

        if not access_token:
            raise HTTPError(status_code=401)

        spotify_user = await spotify_service.get_spotify_user(access_token)
        spotify_artists = await spotify_service.get_all_top_artists_for_user(access_token)
        session = Session()
        taxonomy_graph = graph_service.build_taxonomy_graph(session, spotify_user, spotify_artists)

        response = taxonomy_graph.render_as_json()

        return self.write(response)
