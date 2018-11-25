from graph.models import SpotifyArtist, TaxonomyGraph


__all__ = [
    'parse_artists_from_spotify_response',
    'build_taxonomy_graph_from_artists',
]


def parse_artists_from_spotify_response(spotify_response):
    spotify_artists = spotify_response['items']
    return [_parse_artist_from_spotify_artist(artist) for artist in spotify_artists]


def _parse_artist_from_spotify_artist(spotify_artist):
    return SpotifyArtist(
        id=spotify_artist['id'],
        name=spotify_artist['name'],
        genres=spotify_artist['genres'],
    )


def build_taxonomy_graph_from_artists(artists):
    taxonomy_graph = TaxonomyGraph()

    for artist in artists:
        artist_slug = artist.name.lower()
        artist_node = taxonomy_graph.add_node(artist_slug)

        if not artist.genres:
            continue

        genre = artist.genres[0]
        genre_slug = genre.replace(' ', '-')

        if genre_slug not in taxonomy_graph:
            genre_node = taxonomy_graph.add_node(genre_slug)
        else:
            genre_node = taxonomy_graph.get_node(genre_slug)

        taxonomy_graph.add_edge(taxonomy_graph.get_root_node(), genre_node)
        taxonomy_graph.add_edge(genre_node, artist_node)

    return taxonomy_graph
