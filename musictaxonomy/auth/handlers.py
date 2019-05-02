import urllib.parse

from musictaxonomy.auth import service as auth_service
from musictaxonomy.auth.models import SpotifyAuthorization
from musictaxonomy.database import Session
from musictaxonomy.handlers import BaseAPIHandler
from musictaxonomy.spotify import constants as spotify_constants
from musictaxonomy.spotify import client as spotify_client
from musictaxonomy.spotify import service as spotify_service
from settings import HOST, SPOTIFY_CLIENT_ID


class LoginHandler(BaseAPIHandler):

    async def get(self):
        """
        Before using Music Taxonomy, a user must authenticate with Spotify's Oauth. This
        endpoint is the first step in that authentication flow. We redirect to Spotify's login
        page, passing query parameters to identify our application and specify which scopes the
        application requires. We also pass a redirect URL parameter, which Spotify will use once
        the user logs in successfully.

        For more information, see:
        https://developer.spotify.com/documentation/general/guides/authorization-guide
        """
        access_token = self.get_access_token()
        is_access_token_valid = await auth_service.is_access_token_valid(access_token)

        # User is already logged in.
        if is_access_token_valid:
            return self.redirect('/', permanent=False)

        query_parameters = {
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': '{}/callback/oauth'.format(HOST),
            'scope': 'user-top-read',
        }
        spotify_authorize_url = '{base}?{query_string}'.format(
            base=spotify_constants.SPOTIFY_AUTHORIZE_URL,
            query_string=urllib.parse.urlencode(query_parameters),
        )

        return self.redirect(spotify_authorize_url, permanent=False)


class OauthCallbackHandler(BaseAPIHandler):

    async def get(self):
        """
        This endpoint is the second and final step of the authentication flow. At this point
        the user has logged in successfully to Spotify, and the user has been redirected back to
        Music Taxonomy with an authorization code. We exchange this authorization code for an
        access token by making a request to Spotify, passing our application's credentials. Once
        we receive the access token, we redirect to the IndexHandler so the user can start using
        the application.

        For more information, see:
        https://developer.spotify.com/documentation/general/guides/authorization-guide
        """
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
