from collections import defaultdict

from musictaxonomy.graph import constants as graph_constants
from musictaxonomy.graph.models import MainGenre, TaxonomyGraph

__all__ = [
    'build_taxonomy_graph',
]


def build_taxonomy_graph(session, spotify_user, spotify_artists):
    """
    Args:
        session (Session): A SQLAlchemy session object.
        spotify_user (SpotifyUser): The SpotifyUser of the logged-in user.
        spotify_artists (list): A list of SpotifyArtist objects to add to the graph.

    Returns:
        TaxonomyGraph: A graph associating each aritst with a subgenre and each
            subgenre with a main genre.
    """

    # Initialize a new taxonomy graph.
    taxonomy_graph = TaxonomyGraph(spotify_user.display_name)

    # Retrieve the main genres from the database.
    main_genres = _get_all_main_genres(session)

    # Build a map of spotify genre to number of occurrences of that genre among all artists.
    # This is used to choose an artist's subgenre based on which is the most popular.
    spotify_genre_popularity_map = _get_spotify_genre_popularity_map(spotify_artists)

    spotify_artists = _filter_out_duplicate_spotify_artists(spotify_artists)
    spotify_artists = _filter_out_spotify_artists_without_genres(spotify_artists)

    for spotify_artist in spotify_artists:
        _add_spotify_artist_to_taxonomy_graph(
            session,
            spotify_artist,
            taxonomy_graph,
            main_genres,
            spotify_genre_popularity_map,
        )

    return taxonomy_graph


def _get_all_main_genres(session):
    """
    Main genres are the top-level nodes that have the root as a parent and
    subgenre nodes as children. There is a small, predefined set of these stored
    in the database, they do not come from Spotify.
    """
    return session.query(MainGenre).all()


def _get_spotify_genre_popularity_map(spotify_artists):
    spotify_genre_popularity_map = defaultdict(int)

    for spotify_artist in spotify_artists:
        for spotify_genre in spotify_artist.genres:
            spotify_genre_popularity_map[spotify_genre] += 1

    return spotify_genre_popularity_map


def _filter_out_duplicate_spotify_artists(spotify_artists):
    """
    We should not try to add the same artist multiple times to the graph, so filter
    out any duplicates.
    """
    spotify_artist_dictionary = {
        spotify_artist.id: spotify_artist
        for spotify_artist in spotify_artists
    }

    return list(spotify_artist_dictionary.values())


def _filter_out_spotify_artists_without_genres(spotify_artists):
    """
    We need at least one genre to add an artist to the graph, so filter out artists that
    Spotify returned with an empty genre list.
    """
    return [
        spotify_artist for spotify_artist in spotify_artists
        if len(spotify_artist.genres) > 0
    ]


def _add_spotify_artist_to_taxonomy_graph(session, spotify_artist, taxonomy_graph,
                                          main_genres, spotify_genre_popularity_map):
    main_genre_name = _choose_best_main_genre_name_for_artist(spotify_artist, main_genres)
    subgenre_name = _choose_best_subgenre_name_for_artist(
        spotify_artist,
        main_genre_name,
        main_genres,
        spotify_genre_popularity_map,
    )

    # We could not find a subgenre for the artist, so skip adding them to the graph.
    if subgenre_name is None:
        return None

    main_genre_node = _get_or_create_main_genre_node(main_genre_name, taxonomy_graph)
    subgenre_node = _get_or_create_subgenre_node(subgenre_name, taxonomy_graph, main_genre_node)
    artist_node = taxonomy_graph.add_artist_node(spotify_artist.id, spotify_artist.name)
    taxonomy_graph.add_subgenre_to_artist_edge(subgenre_node, artist_node)

    return artist_node


def _choose_best_main_genre_name_for_artist(spotify_artist, main_genres):
    if 'pop' in spotify_artist.genres and 'edm' in spotify_artist.genres:
        return 'Electronic'

    matching_functions = [
        _exact_match,
        _best_substring_match,
        _subgenre_alias_match,
    ]

    for matching_function in matching_functions:
        main_genre_name = matching_function(spotify_artist.genres, main_genres)
        if main_genre_name is not None:
            return main_genre_name

    return graph_constants.MAIN_GENRE_UNKNOWN


def _exact_match(spotify_genres, main_genres):
    for spotify_genre in spotify_genres:
        for main_genre in main_genres:
            if main_genre.spotify_name == spotify_genre:
                return main_genre.display_name

    return None


def _best_substring_match(spotify_genres, main_genres):
    main_genre_substring_matches = defaultdict(int)

    for spotify_genre in spotify_genres:
        for main_genre in main_genres:
            if main_genre.spotify_name in spotify_genre:
                main_genre_substring_matches[main_genre.display_name] += 1

    if len(main_genre_substring_matches) > 0:
        main_genre_name = max(
            main_genre_substring_matches.keys(),
            key=lambda key: main_genre_substring_matches[key]
        )
        return main_genre_name

    return None


def _subgenre_alias_match(spotify_genres, _):
    for spotify_genre in spotify_genres:
        for subgenre, main_genre_name in graph_constants.SUBGENRE_TO_MAIN_GENRE_ALIASES.items():
            if subgenre in spotify_genre:
                return main_genre_name

    return None


def _choose_best_subgenre_name_for_artist(spotify_artist, main_genre_name,
                                          main_genres, spotify_genre_popularity_map):
    spotify_artist_genres = _filter_out_main_genres(spotify_artist.genres, main_genres)
    subgenre_name = _choose_subgenre_name_from_spotify_genres(
        main_genre_name,
        spotify_artist_genres,
        spotify_genre_popularity_map,
    )

    return subgenre_name


def _filter_out_main_genres(spotify_arist_genres, main_genres):
    main_genre_spotify_names = {main_genre.spotify_name for main_genre in main_genres}
    return [genre for genre in spotify_arist_genres if genre not in main_genre_spotify_names]


def _choose_subgenre_name_from_spotify_genres(main_genre, spotify_genres,
                                              spotify_genre_popularity_map):
    if len(spotify_genres) == 0:
        return None

    spotify_genres_sorted_by_popularity = sorted(
        spotify_genres,
        key=lambda x: spotify_genre_popularity_map[x],
        reverse=True,
    )

    return spotify_genres_sorted_by_popularity[0]


def _get_or_create_main_genre_node(main_genre_name, taxonomy_graph):
    """
    Return the node for the main genre if it exists, otherwise create a new node and
    make it a child of the root node.
    """
    if main_genre_name in taxonomy_graph:
        main_genre_node = taxonomy_graph.get_node(main_genre_name)
    else:
        main_genre_node = taxonomy_graph.add_genre_node(main_genre_name)
        taxonomy_graph.add_edge(taxonomy_graph.get_root_node(), main_genre_node)

    return main_genre_node


def _get_or_create_subgenre_node(subgenre_name, taxonomy_graph, main_genre_node):
    """
    Return the node for the subgenre if it exists, otherwise create a new node and
    make it a child of the given main genre node.
    """
    if subgenre_name in taxonomy_graph:
        subgenre_node = taxonomy_graph.get_node(subgenre_name)
    else:
        subgenre_node = taxonomy_graph.add_subgenre_node(subgenre_name, subgenre_name.title())
        taxonomy_graph.add_genre_to_subgenre_edge(main_genre_node, subgenre_node)

    return subgenre_node
