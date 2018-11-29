from graph.models import TaxonomyGraph


__all__ = [
    'build_taxonomy_graph_from_spotify_artists',
]


def build_taxonomy_graph_from_spotify_artists(artists):
    taxonomy_graph = TaxonomyGraph()

    for artist in artists:
        artist_slug = artist.name.lower()

        # Skip an artist if they already exist in the graph.
        if artist_slug in taxonomy_graph:
            continue

        artist_node = taxonomy_graph.add_node(artist_slug)

        # Skip an artist if they do not have any associated genres.
        if not artist.genres:
            continue

        genre = artist.genres[0]

        if genre not in taxonomy_graph:
            genre_node = taxonomy_graph.add_node(genre)
        else:
            genre_node = taxonomy_graph.get_node(genre)

        taxonomy_graph.add_edge(taxonomy_graph.get_root_node(), genre_node)
        taxonomy_graph.add_edge(genre_node, artist_node)

    return taxonomy_graph
