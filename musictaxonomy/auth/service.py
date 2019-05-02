from tornado.httpclient import HTTPClientError

from musictaxonomy.auth.models import User
from musictaxonomy.database import Session
from musictaxonomy.spotify import client as spotify_client
from musictaxonomy.spotify import service as spotify_service


__all__ = [
    'get_spotify_access_token',
    'is_access_token_valid',
    'create_new_user_if_necessary',
]


async def get_spotify_access_token(authorization_code):
    access_token_response = await spotify_client.get_access_token(
        authorization_code
    )

    return access_token_response['access_token']


async def is_access_token_valid(access_token):
    if not access_token:
        return False

    try:
        await spotify_client.get_current_user_profile(access_token)
    except HTTPClientError:
        return False

    return True


async def create_new_user_if_necessary(access_token):
    spotify_user = await spotify_service.get_spotify_user(access_token)
    session = Session()

    if not _does_spotify_user_exist(session, spotify_user):
        _create_user_from_spotify_user(
            session,
            spotify_user,
            should_commit=True,
        )


def _does_spotify_user_exist(session, spotify_user):
    return session.query(User) \
        .filter_by(external_id=spotify_user.id, external_source='spotify') \
        .count() > 0


def _create_user_from_spotify_user(session, spotify_user, should_commit=False):
    user = User(
        display_name=spotify_user.display_name,
        external_source='spotify',
        external_id=spotify_user.id,
    )
    session.add(user)

    if should_commit:
        session.commit()

    return User
