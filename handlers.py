import json

from tornado.web import RequestHandler


class BaseAPIHandler(RequestHandler):

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
