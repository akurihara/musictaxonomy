import json

from tornado.web import RequestHandler


class IndexHandler(RequestHandler):

    def get(self):
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
            'version': '1.0.0',
        }

        return self.write(response)
