from collections import defaultdict

from graph.models import Genre, TaxonomyGraph


__all__ = [
    'build_taxonomy_graph_from_spotify_artists',
]


def build_taxonomy_graph_from_spotify_artists(session, spotify_artists):
    taxonomy_graph = TaxonomyGraph()
    main_genres = _get_all_main_genres(session)

    for spotify_artist in spotify_artists:
        # Skip an spotify_artist if they already exist in the graph.
        if spotify_artist.id in taxonomy_graph:
            continue

        # Skip an spotify_artist if they do not have any associated genres.
        if not spotify_artist.genres:
            continue

        artist_node = taxonomy_graph.add_artist_node(
            spotify_artist.id,
            spotify_artist.name,
        )

        genre, subgenre = _choose_best_genre_and_subgenre_for_artist(
            session,
            spotify_artist,
            main_genres,
        )

        if genre not in taxonomy_graph:
            genre_node = taxonomy_graph.add_genre_node(genre)
            taxonomy_graph.add_edge(taxonomy_graph.get_root_node(), genre_node)
        else:
            genre_node = taxonomy_graph.get_node(genre)

        if subgenre is None:
            taxonomy_graph.add_genre_to_artist_edge(genre_node, artist_node)
        else:
            if subgenre not in taxonomy_graph:
                subgenre_node = taxonomy_graph.add_subgenre_node(subgenre, subgenre.title())
                taxonomy_graph.add_genre_to_subgenre_edge(genre_node, subgenre_node)
            else:
                subgenre_node = taxonomy_graph.get_node(subgenre)

            taxonomy_graph.add_subgenre_to_artist_edge(subgenre_node, artist_node)

    return taxonomy_graph


def _choose_best_genre_and_subgenre_for_artist(session, spotify_artist, main_genres):
    main_genre = _choose_main_genre_from_spotify_genres(main_genres, spotify_artist.genres)
    spotify_artist_genres = _filter_out_main_genres(spotify_artist.genres, main_genres)
    subgenre = _choose_subgenre_from_spotify_genres(main_genre, spotify_artist_genres)

    return main_genre, subgenre


def _get_all_main_genres(session):
    return session.query(Genre).all()


def _choose_main_genre_from_spotify_genres(main_genres, spotify_genres):
    main_genre_substring_matches = defaultdict(int)

    if 'pop' in spotify_genres and 'edm' in spotify_genres:
        return 'Electronic'

    for main_genre in main_genres:
        for spotify_genre in spotify_genres:
            if main_genre.spotify_name == spotify_genre:
                return main_genre.display_name
            elif main_genre.spotify_name in spotify_genre:
                main_genre_substring_matches[main_genre.display_name] += 1

    if main_genre_substring_matches:
        main_genre = max(
            main_genre_substring_matches.keys(),
            key=lambda key: main_genre_substring_matches[key]
        )
        return main_genre

    return 'Unknown'


def _filter_out_main_genres(spotify_arist_genres, main_genres):
    main_genre_spotify_names = {main_genre.spotify_name for main_genre in main_genres}
    return [genre for genre in spotify_arist_genres if genre not in main_genre_spotify_names]


def _choose_subgenre_from_spotify_genres(main_genre, spotify_genres):
    if len(spotify_genres) == 0:
        return None

    for spotify_genre in spotify_genres:
        if main_genre != spotify_genre and main_genre in spotify_genre:
            return spotify_genre

    return spotify_genres[0]
