import urllib.parse
from typing import Optional

from musictaxonomy.auth.models import User
from musictaxonomy.database import Session
from musictaxonomy.spotify import client as spotify_client
from musictaxonomy.spotify import constants as spotify_constants
from musictaxonomy.spotify.models import SpotifyUser
from settings import SPOTIFY_CLIENT_ID
from tornado.httpclient import HTTPClientError

__all__ = [
    "generate_spotify_authorize_url",
    "get_spotify_access_token",
    "is_access_token_valid",
    "create_new_user_if_necessary",
]


def generate_spotify_authorize_url(redirect_base_url: str) -> str:
    query_parameters = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "{}/callback/oauth".format(redirect_base_url),
        "scope": "user-top-read",
    }
    spotify_authorize_url = "{base}?{query_string}".format(
        base=spotify_constants.SPOTIFY_AUTHORIZE_URL,
        query_string=urllib.parse.urlencode(query_parameters),
    )

    return spotify_authorize_url


async def get_spotify_access_token(
    authorization_code: str, redirect_base_url: str
) -> str:
    access_token_response = await spotify_client.get_access_token(
        authorization_code, redirect_base_url
    )

    return access_token_response["access_token"]


async def is_access_token_valid(access_token: str) -> bool:
    if not access_token:
        return False

    try:
        await spotify_client.get_current_user_profile(access_token)
    except HTTPClientError:
        return False

    return True


async def create_new_user_if_necessary(spotify_user: SpotifyUser) -> Optional[User]:
    session = Session()
    user = None

    if not _does_spotify_user_exist(session, spotify_user):
        user = _create_user_from_spotify_user(session, spotify_user, should_commit=True)

    return user


def _does_spotify_user_exist(session: Session, spotify_user: SpotifyUser) -> bool:
    """
    Check if the given SpotifyUser object has corresponding User row stored in the database.
    """
    number_of_users = (
        session.query(User)
        .filter_by(external_id=spotify_user.id, external_source="spotify")
        .count()
    )
    return number_of_users > 0


def _create_user_from_spotify_user(
    session: Session, spotify_user: SpotifyUser, should_commit: bool = False
) -> User:
    """
    Create a User row in the database from the given SpotifyUser object.
    """
    user = User(
        display_name=spotify_user.display_name,
        external_source="spotify",
        external_id=spotify_user.id,
    )
    session.add(user)

    if should_commit:
        session.commit()

    return user
