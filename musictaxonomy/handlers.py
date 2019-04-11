import json

from tornado.web import RequestHandler

from musictaxonomy.auth import service as auth_service


class IndexHandler(RequestHandler):

    async def get(self):
        access_token = self.get_secure_cookie('AccessToken')
        if access_token:
            is_access_token_valid = await auth_service.is_access_token_valid(access_token.decode('ascii'))
            if not is_access_token_valid:
                return self.redirect('/login', permanent=False)
        else:
            return self.redirect('/login', permanent=False)


        self.render('index.html')


class BaseAPIHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header("Access-Control-Allow-Headers", 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'application/json')
        response_body = {
            'error': {
                'code': status_code,
                'message': self._reason,
            }
        }

        return self.finish(json.dumps(response_body))


class StatusHandler(BaseAPIHandler):

    def get(self):
        response = {
            'message': 'ok',
            'status': 200,
        }

        return self.write(response)
