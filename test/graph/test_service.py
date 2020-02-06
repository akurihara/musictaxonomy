from unittest import TestCase

from musictaxonomy.database import Session
from musictaxonomy.graph import service as graph_service
from musictaxonomy.spotify.models import SpotifyArtist, SpotifyUser


class BuildTaxonomyGraphTest(TestCase):
    def test_build_taxonomy_graph_with_unknown_main_genre(self):
        session = Session()
        spotify_user = SpotifyUser(id="1220628328", display_name="Alex Kuriahra")
        spotify_artist = SpotifyArtist(
            id="3TVXtAsR1Inumwj472S9r4", name="Drake", genres=["foo"]
        )

        taxonomy_graph = graph_service.build_taxonomy_graph(
            session, spotify_user, [spotify_artist]
        )

        self.assertIsNotNone(taxonomy_graph.get_node("Unknown"))
