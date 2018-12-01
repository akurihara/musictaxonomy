from collections import defaultdict

from graph.models import Genre, TaxonomyGraph


__all__ = [
    'build_taxonomy_graph_from_spotify_artists',
]


def build_taxonomy_graph_from_spotify_artists(session, spotify_artists):
    taxonomy_graph = TaxonomyGraph()

    for spotify_artist in spotify_artists:
        # Skip an spotify_artist if they already exist in the graph.
        if spotify_artist.name in taxonomy_graph:
            continue

        artist_node = taxonomy_graph.add_node(spotify_artist.name)

        # Skip an spotify_artist if they do not have any associated genres.
        if not spotify_artist.genres:
            continue

        genre, subgenre = _choose_best_genre_and_subgenre_for_artist(session, spotify_artist)

        if genre not in taxonomy_graph:
            genre_node = taxonomy_graph.add_node(genre)
            taxonomy_graph.add_edge(taxonomy_graph.get_root_node(), genre_node)
        else:
            genre_node = taxonomy_graph.get_node(genre)

        if subgenre not in taxonomy_graph:
            subgenre_node = taxonomy_graph.add_node(subgenre)
            taxonomy_graph.add_edge(genre_node, subgenre_node)
        else:
            subgenre_node = taxonomy_graph.get_node(subgenre)

        taxonomy_graph.add_edge(subgenre_node, artist_node)

    return taxonomy_graph


def _choose_best_genre_and_subgenre_for_artist(session, spotify_artist):
    main_genres = _get_all_main_genres(session)
    main_genre = _choose_main_genre_from_spotify_genres(main_genres, spotify_artist.genres)
    subgenre = _choose_subgenre_from_spotify_genres(main_genre, spotify_artist.genres)

    return main_genre, subgenre


def _get_all_main_genres(session):
    return session.query(Genre).all()


def _choose_main_genre_from_spotify_genres(main_genres, spotify_genres):
    main_genre_substring_matches = defaultdict(int)

    for main_genre in main_genres:
        for spotify_genre in spotify_genres:
            if main_genre.spotify_name == spotify_genre:
                return main_genre.spotify_name
            elif main_genre.spotify_name in spotify_genre:
                main_genre_substring_matches[main_genre.spotify_name] += 1

    if main_genre_substring_matches:
        main_genre = max(
            main_genre_substring_matches.keys(),
            key=lambda key: main_genre_substring_matches[key]
        )
        return main_genre

    return 'Unknown'


def _choose_subgenre_from_spotify_genres(main_genre, spotify_genres):
    for spotify_genre in spotify_genres:
        if main_genre != spotify_genre and main_genre in spotify_genre:
            return spotify_genre

    return spotify_genres[0]
