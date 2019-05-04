from musictaxonomy.auth import service as auth_service
from musictaxonomy.handlers import BaseAPIHandler


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

        # User is already logged in, so redirect them to the core application.
        if is_access_token_valid:
            return self.redirect('/', permanent=False)

        redirect_base_url = '{protocol}://{host}'.format(
            protocol=self.request.protocol,
            host=self.request.host,
        )
        spotify_authorize_url = auth_service.generate_spotify_authorize_url(redirect_base_url)

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

        # Exchange the authorization code for an access token from Spotify.
        redirect_base_url = '{protocol}://{host}'.format(
            protocol=self.request.protocol,
            host=self.request.host,
        )
        access_token = await auth_service.get_spotify_access_token(
            authorization_code,
            redirect_base_url,
        )

        # Set the access token as a cookie.
        self.set_secure_cookie('AccessToken', access_token)

        # Create a new User in the database if one does not already exist.
        await auth_service.create_new_user_if_necessary(access_token)

        # Redirect the user to the core application.
        return self.redirect('/', permanent=False)
