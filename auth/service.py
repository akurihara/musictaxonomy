from auth.models import User


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
