from unittest import TestCase

from musictaxonomy.spotify.models import SpotifyArtist, SpotifyUser


class SpotifyArtistTest(TestCase):
    def test_conversion_to_string(self):
        spotify_artist = SpotifyArtist(
            id="3TVXtAsR1Inumwj472S9r4",
            name="Drake",
            genres=["hip hop", "pop rap", "rap"],
        )

        self.assertEqual(str(spotify_artist), "3TVXtAsR1Inumwj472S9r4")


class SpotifyUserTest(TestCase):
    def test_conversion_to_string(self):
        spotify_user = SpotifyUser(id="1220628328", display_name="Alex Kuriahra")

        self.assertEqual(str(spotify_user), "1220628328")
