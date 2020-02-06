import json

from musictaxonomy.auth import service as auth_service
from tornado.web import RequestHandler


class BaseAPIHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def write_error(self, status_code, **kwargs):
        self.set_header("Content-Type", "application/json")
        response_body = {"error": {"code": status_code, "message": self._reason}}

        return self.finish(json.dumps(response_body))

    def get_access_token(self):
        """
        Get the value of the `AccessToken` cookie included in the client request. Tornado's
        function to retrieve secure cookies return the value as a bytestring, so convert the
        value to ASCII before returning.
        """
        access_token = self.get_secure_cookie("AccessToken")
        access_token = access_token.decode("ascii") if access_token else None

        return access_token


class IndexHandler(BaseAPIHandler):
    async def get(self):
        """
        The IndexHandler serves HTML containing the Javascript single-page application. The
        application calls the `GET /taxonomy_graphs` endpoint to load the user's taxonomy
        graph.
        """
        access_token = self.get_access_token()
        is_access_token_valid = await auth_service.is_access_token_valid(access_token)

        # User is not logged in, redirect to login endpoint.
        if not is_access_token_valid:
            return self.redirect("/login", permanent=False)

        self.render("index.html")


class StatusHandler(BaseAPIHandler):
    def get(self):
        """
        The status endpoint can be used to quickly check on the health of the application.
        """
        response = {"message": "ok", "status": 200}

        return self.write(response)
