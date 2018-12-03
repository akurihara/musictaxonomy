from spotify import client as spotify_client
from spotify.models import SpotifyArtist, SpotifyUser


__all__ = [
    'get_spotify_user',
    'get_all_top_artists_for_user',
]


async def get_spotify_user(access_token: str):
    user_profile_response = await spotify_client.get_current_user_profile(access_token)
    spotify_user = SpotifyUser(
        id=user_profile_response['id'],
        display_name=user_profile_response['display_name'],
    )

    return spotify_user


async def get_all_top_artists_for_user(access_token: str):
    futures = [
        spotify_client.get_top_artists_in_time_range(access_token, time_range)
        for time_range in ('short_term', 'medium_term', 'long_term')
    ]
    responses = [await future for future in futures]

    return [
        spotify_artist
        for response in responses
        for spotify_artist in _parse_spotify_artists_from_top_artists_response(response)
    ]


def _parse_spotify_artists_from_top_artists_response(response):
    artist_documents = response['items']
    return [_parse_spotify_artist_from_artist_document(document) for document in artist_documents]


def _parse_spotify_artist_from_artist_document(artist_document):
    return SpotifyArtist(
        id=artist_document['id'],
        name=artist_document['name'],
        genres=artist_document['genres'],
    )
