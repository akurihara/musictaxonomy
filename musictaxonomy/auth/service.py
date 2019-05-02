from tornado.httpclient import HTTPClientError

from musictaxonomy.auth.models import User
from musictaxonomy.spotify import client as spotify_client


async def is_access_token_valid(access_token):
    if not access_token:
        return False

    try:
        await spotify_client.get_current_user_profile(access_token)
    except HTTPClientError:
        return False

    return True


def does_spotify_user_exist(session, spotify_user):
    return session.query(User) \
        .filter_by(external_id=spotify_user.id, external_source='spotify') \
        .count() > 0


def get_user_from_spotify_user(session, spotify_user):
    return session.query(User) \
        .filter_by(external_id=spotify_user.id, external_source='spotify') \
        .first()


def create_user_from_spotify_user(spotify_user):
    return User(
        display_name=spotify_user.display_name,
        external_source='spotify',
        external_id=spotify_user.id,
    )
