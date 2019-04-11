import urllib.parse

from musictaxonomy.auth import service as auth_service
from musictaxonomy.auth.models import SpotifyAuthorization
from musictaxonomy.database_utils import Session
from musictaxonomy.handlers import BaseAPIHandler
from musictaxonomy.spotify import constants as spotify_constants
from musictaxonomy.spotify import client as spotify_client
from musictaxonomy.spotify import service as spotify_service
from settings import SPOTIFY_CLIENT_ID


class LoginHandler(BaseAPIHandler):

    def get(self):
        access_token = self.get_secure_cookie('AccessToken')
        if access_token:
            return self.redirect('/', permanent=False)

        query_parameters = {
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': 'http://localhost:8080/callback/oauth',
            'scope': 'user-top-read',
        }
        spotify_authorize_url = '{base}?{query_string}'.format(
            base=spotify_constants.SPOTIFY_AUTHORIZE_URL,
            query_string=urllib.parse.urlencode(query_parameters),
        )

        return self.redirect(spotify_authorize_url, permanent=False)


class OauthCallbackHandler(BaseAPIHandler):

    async def get(self):
        authorization_code = self.get_argument('code')
        access_token_response = await spotify_client.get_access_token(
            authorization_code
        )
        access_token = access_token_response['access_token']
        refresh_token = access_token_response['refresh_token']

        spotify_user = await spotify_service.get_spotify_user(access_token)

        session = Session()
        if not auth_service.does_spotify_user_exist(session, spotify_user):
            user = auth_service.create_user_from_spotify_user(spotify_user)
            session.add(user)
            session.commit()
        else:
            user = auth_service.get_user_from_spotify_user(session, spotify_user)

        spotify_authorization = SpotifyAuthorization(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
        )

        session.add(spotify_authorization)
        session.commit()

        self.set_secure_cookie('AccessToken', access_token)

        return self.redirect('/', permanent=False)
